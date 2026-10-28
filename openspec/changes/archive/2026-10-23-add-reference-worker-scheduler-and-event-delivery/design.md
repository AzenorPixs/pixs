# Conception — C09

## Statut et périmètre autorisé

PRÉPARATION_DOCUMENTAIRE. L’inventaire et la création du dossier sont autorisés ; aucune implémentation ni décision technique encore absente n’est réputée validée. C00 a été adopté et archivé le 18 octobre 2026 ; ses précisions normatives sont intégrées au canon. Les arbitrages propres au présent change restent à lever avant réalisation.

## État actuel vérifié

Constat : JobRecord et des primitives transactionnelles Bulk existent ; ils ne fournissent pas le worker et scheduler généraux ni une livraison d’événements qualifiée.

Sources consultées et empreintes recoupées avec la matrice :

- [src/pixs/backend/models.py](../../../../src/pixs/backend/models.py).
- [src/pixs/kernel/jobs.py](../../../../src/pixs/kernel/jobs.py).
- [src/pixs/kernel/event_registration.py](../../../../src/pixs/kernel/event_registration.py).
- [src/pixs/backend/bulk_runtime_repository.py](../../../../src/pixs/backend/bulk_runtime_repository.py).

Ces constats ne sont pas des preuves d’exécution actuelle des tests. Les structures et sous-lots présents sont à réutiliser ; aucun manque d’intégration ne justifie leur recréation.

## Architecture proposée

Réutiliser les structures applicables sans généraliser un bail Bulk au scheduler. Exécuter jobs et publication après commit via mêmes contrats, persistance PostgreSQL et contexte réautorisé. Lease persistant et clôture de péremption empêchent l’ancien scheduler d’agir ; reprises, retries et états terminaux sont inspectables.

## Alternatives et frontière de conception

Privilégier les mécanismes et dépendances existants. Une implémentation locale qui duplique les contrats, importe des tables privées ou sélectionne implicitement un provider est incompatible avec le cadrage. Toute technologie supplémentaire ou précision de comportement devra être justifiée avant réalisation ; la présence d’un paquet dans DEVOPS ne prouve ni sélection ni conformité.

## Décisions bloquantes avant réalisation

Contrats d’exécution, baux/échéances/fencing, réveil et publication à qualifier. Aucun broker externe ou dépendance ajoutée implicitement ; tout consommateur choisi doit satisfaire sa conformité.

Ce sont des barrières de conception explicites, pas des questions supposées résolues. Elles n’empêchent pas la préparation documentaire ; elles empêchent de présenter le dossier comme entièrement prêt à coder. Les arbitrages PA/PZT suivent TECHNICAL §45.4 lorsqu’ils entrent dans son périmètre.

## Dépendances et progression

Les dossiers suivants doivent fournir leurs contrats/conditions avant intégration :

- [integrate-runtime-authorization-and-super-admin](../2026-10-21-integrate-runtime-authorization-and-super-admin/proposal.md).
- [add-durable-minimized-audit](../2026-10-21-add-durable-minimized-audit/proposal.md).
- [add-protected-core-http-commands-and-queries](../2026-10-22-add-protected-core-http-commands-and-queries/proposal.md).
- [activate-reference-runtime-composition](../2026-10-21-activate-reference-runtime-composition/proposal.md).

La création anticipée de ces dossiers ne signifie pas que leurs tâches sont réalisées. Les hôtes intermédiaires demeurent non prêts si une obligation manque ; C17 qualifie le paquet C18, C19 vérifie son identité de distribution.

## Vérification future et limites

Deux schedulers → un détenteur admissible ; ancien détenteur rejeté ; crash/reprise sans double effet ; événement jamais avant commit ; révocation avant exécution respectée ; drain borné.

Relier les scénarios de `requirements.md` à la recette concernée et conserver versions, verdicts et preuves sans secret. Une unité réussie ne remplace pas une intégration réelle ; un contrat structurel ne confère pas de privilège ni de disponibilité. Les contrôles applicatifs conservent l’exception Super Admin du canon dans son seul périmètre, sans fabrication de fait absent.

## Migrations et retour

Aucune migration ni remise à zéro pendant cette préparation. Toute évolution future de données aura un contrat, un plan autorisé, des contrôles de compatibilité et une compensation/restauration explicite ; aucun abaissement automatique de base.

## Hors profil

PA actif, réseau PZT actif, service DNS exécuté par PA, image Docker et capacités optionnelles restent hors sélection, sauf obligation applicable démontrée imposant de revoir C00 avant qualification.

## Approfondissement issu de l’audit du 17 octobre 2026

Conception proposée sans implémentation. Ces contrats de travail ne modifient pas le canon ; tout changement normatif requiert son delta approuvé.

Pour O21, fournir schémas publics d’événements et versions compatibles avec les enveloppes réellement émises. Les représentations Python déclaratives et records Bulk existants ne démontrent pas un catalogue machine-readable des contrats publics.

Lier producteur propriétaire, type/version, contexte autorisé, corrélation, idempotence, politique de compatibilité et schéma du payload. Ne pas exposer modèles privés ou données de sécurité dans le bundle générable.

C09 conserve émission post-commit, livraison/rejeu et checkpoints ; O21 génère les SDK depuis les schémas publiés. Contrats manquants/divergents bloquent cette génération, sans dépendance inverse vers O21.


Voir [audit individuel et limites des preuves](../2026-10-18-define-first-installable-pbo-profile/audit-ne-94.json) et [rapport d’audit](../../../../reports/audit-ne-94-2026-10-17/RAPPORT.md). Les tâches de réalisation restent non cochées.


## Revue transversale P0 du 17 octobre 2026

Analyse de préparation sans implémentation ; les critères ci-dessous complètent la recette future et ne constituent pas des résultats exécutés. Les décisions de technologie et de paramètres restent ouvertes avant code.

### T03 — Réadmission après état restauré

La restauration cohérente de données ne prouve ni fraîcheur de révocations/incidents ni admissibilité des effets différés. N05 dédié et delta ciblé validés ; faits nécessaires et revalidation détaillée à définir avant code.

Contrôles à intégrer : Snapshot antérieur à révocation/rotation/incident ; Effet déjà engagé dont réponse perdue ; Marqueur externe incohérent ; Interruption puis reprise de réconciliation sans réémission automatique.

### T06 — Marqueurs externes et états PostgreSQL

Marqueur d’installation et marqueur de désactivation Super Admin ont des fonctions différentes et ne sont pas une transaction atomique avec PostgreSQL. Compléter C08 et les contrats C03/C04/C09 ; N05 vérifie le rapprochement après restauration.

Contrôles à intégrer : Commit base avant marqueur : reprise sans second compte ; Marqueur absent/invalide interdit NORMAL sans relancer INSTALLER ; Désactivation non dérogée refuse nouvelles actions/reprises, transaction engagée préservée ; Secours propre sans MFA imposé.

### T10 — Mutation, audit, idempotence et outbox

Les composants prévoient chacun leur partie ; la frontière transactionnelle et l’échec avant/après commit doivent être explicitement communs. Compléter contrats C05/C06/C09 avec refus distincts et résultat réconcilié ; pas de nouveau broker.

Contrôles à intégrer : Rollback sans événement publié ; Commit puis réponse perdue restituant résultat idempotent ; Double livraison sans double effet propriétaire ; Refus auditable sans mutation métier.

### T11 — Arrêt, maintenance et ancien détenteur de lease

Le séquencement des nouvelles admissions, du drain et des reprises est une interaction ; un timeout du processus ne prouve pas la fin d’un effet. Compléter recette commune C09/C15/C18 ; pas de nouvel orchestrateur.

Contrôles à intégrer : Lease expiré empêchant une nouvelle action ; Maintenance ciblée et install entière distinguées ; Signal pendant effet, sortie explicite sans perte silencieuse ; Worker non public.

### T16 — Options, profils structurels et renvois Bulk

Un rattachement à un lot P0 n’active pas tout le domaine : Bulk, LDAP, flags avancés, quotas, SDK, sandbox et intégrité avancée restent conditionnés. Déclarer sélection/absence et maintenir les profils structurels existants ; ne pas traiter la non-sélection comme dispense d’une clause applicable.

Contrôles à intégrer : Absent représenté sans readiness fictive ; Contrat consommé réutilisé sans activer tout le catalogue ; Aucun code distant ni composant DEVELOPMENT en production ; Pas de promesse universelle de performance/HA.

Voir [audit transversal durable](../2026-10-18-define-first-installable-pbo-profile/audit-transversal-p0.json) et [rapport local](../../../../reports/audit-transversal-p0-2026-10-17/RAPPORT.md). Aucune tâche de réalisation cochée.

## Décisions C09 validées par le développeur — RSMP du 22 octobre 2026

Le RUN CISMP2 est autorisé à réaliser ce seul change, puis à l'archiver, produire et vérifier son rapport STATISTIQUES.md et s'arrêter de façon ciblée. Le statut PRÉPARATION_DOCUMENTAIRE et les interdictions de réalisation des paragraphes historiques décrivent leur autorisation d'origine. La présente validation lève les choix ci-dessous pour C09 ; elle ne déclare aucune tâche réalisée et n'étend pas le canon. La reprise RSMP est limitée à ce document et requirements.md ; elle ne produit ni code ni coche.

### D1 — Propriétaires et coordination PostgreSQL

PostgreSQL constitue la persistance de référence et la coordination du worker, du scheduler et de la publication ; aucun broker externe ni dépendance nouvelle n'est sélectionné. Réutiliser JobRecord, JobState et les contrats publics réellement applicables. Conserver les profils préparatoires et leurs limites ; porter les métadonnées d'exécution, de planning, de déduplication et les révisions dans des extensions runtime propriétaires distinctes des tables Bulk.

Le Kernel conserve les mécanismes et contrats déclaratifs. Les exécutants, repositories PostgreSQL, adaptateurs et boucles PBO restent au-dessus du Kernel. Les modules propriétaires réalisent seuls leurs mutations via leurs contrats publics. Un consommateur d'événement ou handler versionné doit être explicitement déclaré et validé ; sa présence ne confère aucun droit ni aucune conformité.

### D2 — Réveil et politique explicites

Le scheduler utilise un polling borné, sous configuration explicite versionnée. Les politiques fournissent les baux, renouvellements, échéances, tentatives et délais, bornes de polling, concurrence, taille des unités, drain et budgets nécessaires. Aucun défaut numérique produit n'est ajouté par cette décision. Une politique absente, étrangère, non bornée, contradictoire ou non résolue refuse l'admission ; les valeurs de fixtures sont synthétiques et ne deviennent pas des valeurs produit.

Les rôles web, worker et scheduler sont ceux du même artefact PBO. Les plans de processus et de concurrence respectent le budget réellement accordé à leur environnement et les plafonds PostgreSQL ; aucun nombre de workers n'est déduit du seul nombre de cœurs. Distinguer plan demandé, capacités sélectionnées et état observé. Les contrôles ou adaptations non qualifiés ne sont pas annoncés disponibles et ne deviennent pas un repli permissif.

### D3 — Baux, autorisation et reprise

Le bail scheduler est persistant, borné et renouvelable, avec propriétaire, expiration, révision et fencing empêchant l'ancien détenteur de déclencher une nouvelle unité. Le bail d'un Job et celui du scheduler ont des propriétaires et responsabilités distincts. La politique de renouvellement laisse une marge vérifiable avant expiration ; une perte de bail ferme les nouvelles unités sans prolongation implicite ni annulation fictive d'un effet déjà engagé.

Chaque travail conserve l'acteur initial, les références de contexte, corrélation, causalité, opération et commande distinctes. Aucun credential ni privilège du demandeur n'est transféré au worker. L'admission et l'exécution utilisent les contrats publics d'autorisation courants ; les faits manquants, expirés ou non vérifiables produisent un refus fermé. L'exception Super Admin demeure celle du canon et sa désactivation non dérogée refuse une nouvelle exécution ou reprise.

Les états PENDING, SCHEDULED, RUNNING, SUCCEEDED, RETRYING, FAILED, PAUSED, CANCELLED et DEAD_LETTER restent explicites et persistants. Les tentatives et délais sont bornés, les rejets métier se distinguent des erreurs techniques rejouables, et le checkpoint engagé détermine la reprise. La fermeture des admissions, le drain borné et la restitution du travail conservent un état diagnostiquable ; silence, timeout ou arrêt de processus ne prouvent jamais la fin d'un effet inconnu. Si la réadmission ou la revalidation requise après restauration manque, aucune réémission automatique n'est admise ; la qualification dédiée N05 n'est pas présumée livrée.

### D4 — Transaction propriétaire, outbox et inbox

L'enveloppe d'événement est immuable, versionnée, minimisée et conforme au schéma public déclaré. Domaine et intégration restent distincts. Mutation et enregistrement outbox partagent la même transaction propriétaire ; aucun événement annulé n'est publiable. Le publisher lit seulement des événements engagés, sous bail et politique bornés, avec états inspectables. La livraison est au-moins-une-fois : une émission suivie d'un crash avant accusé persistant peut être répétée.

Le consommateur déduplique durablement par référence de consommateur et identifiant d'événement ; version et empreinte divergentes sont refusées. Consommation et effets propriétaires sont engagés dans leur frontière transactionnelle commune. Un effet externe ne reçoit une garantie de déduplication que si son provider déclare et prouve l'idempotence requise. L'ordre est limité au périmètre déclaré, avec séquence allouée atomiquement ; un événement antérieur non publié bloque ce périmètre sans bloquer les autres. Aucune promesse exactly-once ni ordre global.

### Validation séquentielle et frontières conservées

Avant code, le contrat de chaque tâche identifie ses fichiers, entrées/sorties, refus, dépendances et tests propres. La tâche 1.1 recoupe les canons courants et leurs scénarios ; 1.2 vérifie ces décisions et les contrats proposés ; 2.1 définit les contrats versionnés et registres, sans boucle active implicite. Les tests nécessaires à 2.2 et 2.3 sont exécutés avec chacune d'elles, notamment PostgreSQL réel pour persistance, concurrence, rollback et reprise. La tâche 2.4 consolide deux schedulers, ancien détenteur, crash/rejeu, révocation et drain ; elle ne remplace pas ces contrôles locaux.

Les interfaces C04/C05/C06/C07 sont réutilisées après relecture ; leurs doubles C09 ne sont pas des exécutants livrés. La réadmission N05, l'installation C08, le cycle de vie C10, les essentiels C14 et la qualification/distribution C17/C18/C19 restent distingués de la preuve propre C09. Une dépendance réellement indispensable et absente ferme le périmètre concerné ; aucune non-sélection ne dispense d'une clause obligatoire. Aucun réseau PA/PZT, transport alternatif, déploiement, Git, nouvelle dépendance ou performance de production n'est autorisé par ces décisions.

## Réalisation C09 — contrats et limites du profil de référence

Cette réalisation reste limitée à C09. Ses preuves ne qualifient pas le P0,
l'installation C08, la réadmission N05, la gouvernance C10, PA/PZT ou la
distribution C17/C19. Aucun canon n'est modifié.

### Organisation, données et transactions

Le Backend porte contrats/registre C09, adaptateur d'autorisation, extensions
de JobRecord, worker et scheduler, événements, outbox/inbox, ressources,
slots, drivers et entrée. Le Kernel reste déclaratif. Aucun import de
table privée Bulk n'est ajouté.

Les migrations additives 0012_c09_jobs et 0013_c09_events_scheduler
conservent les champs existants de JobRecord. Les dix records de 0013
portent coordination, intentions ponctuelles, curseurs, enveloppes,
stage/publication, destinations, réceptions, preuves d'unités et slots.
Contraintes et déclencheurs contrôlent immutabilité, transaction physique,
transitions, ordre et compteurs. Le retour refuse toute donnée présente ;
aucune remise à zéro ou compensation automatique n'est fournie.

Les participants Core C09 conservent les signatures C05/C06/Core et la
transaction durable Core. C09CoreJobUnit lie Job, unité, checkpoint attendu
et produit, complétude, identité, politique et bail. C09CoreInboxUnit lie
événement, consumer, bail de publication et unité. Le décorateur du vrai
participant C06 contrôle ces liaisons avant mutation, puis engage
checkpoint ou reçu et preuve avec les cinq champs du résultat Core,
leur hash, commande, identité, source, opération, token et xid.
L'outbox attachée partage ce commit et dérive un identifiant stable
par opération/entrée.

Le replay vérifie propriétaire, unité, commande et résultat complet C06.
Il ne refait pas la mutation, ne requiert pas de nouveau bail pour un
fait engagé, et ne fait pas régresser un checkpoint ultérieur ou un Job
déjà terminé. Le token de restauration reste distinct du token historique.
Une issue non réconciliée reste fermée.

### Configuration et budgets

C09PolicyV1 exige référence/version, bail et renouvellement, tentatives
et délais, intervalle et lot de polling, concurrence, unités par poll,
drain, échéances de tentative/travail, processus, CPU, connexions, mémoire
et date d'effet. Les entiers sont exacts et bornés, sans booléen admis.
Les marges de renouvellement, l'échéance globale et les lots sont vérifiés.
Aucune valeur numérique produit par défaut n'est créée.

C09DeliveryPolicyV1 ajoute référence/version et plafonds d'enveloppe en
octets, de références de payload, d'événements et de livraisons en attente.
Son hash couvre tous ses champs et ceux de sa base. Le scheduler reçoit
séparément max_pending_schedules et planifie due_at/expires_at ;
aucun cron, récurrence ou rattrapage implicite n'est fourni.

C09RuntimePlanV1 lie propriétaire, environnement, référence/version, rôles
et C09QueueBudgetV1 : Jobs, schedules, événements et livraisons en attente,
octets d'événement, références et buffer. Les plafonds persistants des
files s'appliquent au périmètre/contexte déclaré. C09BoundedJobAdmission et
le driver scheduler partagent le verrou de capacité Jobs. Le scheduler
runtime déclenche une intention par transaction sous ce verrou, avec
max_triggers=1, borné par sa politique. Les primitives isolées ne valent
pas qualification d'un profil complet.

Les cumuls CPU, mémoire, connexions et concurrence sont calculés par nombre
de processus, avec les marges accordées aux dépendances. Le champ historique
memory_mb est interprété en MiB ; les buffers sont en octets. Le profil V1
worker/scheduler sérialise une unité par processus ; les processus sont
explicitement déclarés et supervisés, sans déduction du nombre de cœurs.
Une concurrence supérieure dans ces deux rôles est refusée. Le web borne
ses requêtes actives et refuse la surcharge sans file d'attente en mémoire.

Le plan pur exige au moins 2 * concurrence + 1 connexions par processus ;
l'entrée concrète exige 2 * concurrence + 4 pour unités, contrôle et C07.
Les buffers couvrent les enveloppes du lot et restent sous la mémoire du
rôle. Un plan validé n'est pas une limite OS appliquée. Les observations
séparent détection, budget accordé et application réelle, avec source,
version, révision et validité. Absence, péremption ou application partielle
ferment l'admission. Aucune adaptation, création de processus ou modification
OS/cgroup/conteneur/service n'est implicite.

### Autorité, livraison locale et schémas

Acteur initial, périmètre, ScopeContext et corrélation sont conservés.
Les fonctions de composition serveur lient les références de demande à
C04 courant ; N05 absent, périmé ou divergent refuse. Aucun credential
n'est transporté. Les dérogations Super Admin restent celles de C04,
sans suppression des bornes techniques ; une dérogation d'audit n'est
pas un audit effectué.

JOINED admet seulement une fonction serveur déclarée sans effet externe.
Mutation locale, résultat/checkpoint et reçu partagent la transaction
propriétaire. Un consumer CORE_DURABLE porte uniquement ses métadonnées
avec execute=None ; l'entrée JOINED le refuse. Son exécution passe par
le participant Core concret. Les drivers n'invoquent que des fonctions
Core publiques installées avec les ports C09 attachés.

L'enveloppe est fermée, versionnée, immuable et minimisée ; son payload
contient des références opaques bornées. Les schémas JSON exportables
DOMAIN et INTEGRATION restent distincts, sans modèle privé. Les
décodeurs refusent doublons JSON, types étrangers, UTF-8 invalide,
dates non canoniques et dépassements.

Curseur, événement, stage, publication et destinations sont engagés avec
la mutation propriétaire. Le publisher lit seulement des faits engagés.
Un prédécesseur non publié bloque son périmètre d'ordre ; ce filtrage
intervient avant le lot de polling. Le driver LOCAL exige la couverture
exécutable de tous les consumers de son catalogue.

L'inbox réévalue la demande propre du consumer : publier ne confère pas
le droit de consommer. Le reçu est engagé avec l'effet, par consumer et
événement, avec versions, empreintes, acteur et contexte. L'ACK exige ce
reçu réel. Une perte après son commit et avant ACK peut répéter la
livraison sans second effet confirmé. Aucune garantie exactly-once ou
effet externe n'est revendiquée. FAILED et DEAD_LETTER restent terminaux ;
les remises en attente Bulk conditionnelles ne sont pas activées.

### Entrées, arrêt et reprise

C09RoleEntry exige NORMAL, Django déjà configuré, applications/migrations
requises, deux alias PostgreSQL vers le même schéma et vrai PreparedHostPlan.
Le budget est contrôlé avant acquisition/hooks C07 puis au claim.
Le vrai host_runtime garde ressources, observations et hooks avec
affinité Django. INSTALLER C07 reste distinct ; C09 ne crée aucun resolver
de secret ou configuration Django NORMAL.

Les fonctions serveur d'admission doivent authentifier installation,
réadmission, lifecycle, plan et surface HTTP courants. Les sources de
supervision doivent vérifier budgets et limites réellement appliqués.
Leurs DTO seuls ne sont pas des autorisations ; un port absent reste
non prêt. Worker/scheduler n'exposent ni ASGI ni serveur HTTP. Le web
utilise le vrai handler Django, les middlewares C07 attendus et une
surface validée par son propriétaire ; aucun endpoint métier ou de
management n'est ajouté par C09.

Les slots persistent par environnement/plan/rôle/index avec processus,
bail, génération, révision et unités en cours. Un seul plan est actif
par budget d'environnement ; la reconfiguration attend la quiescence
et conserve l'historique. Un arrêt local restitue seulement les baux
détenus, sans fermer le coordinateur partagé ou arrêter les pairs.

Les signaux sont installés uniquement sur demande explicite du lanceur.
Les unités possédées utilisent un thread daemon et leurs connexions
propres. Le drain réserve une fenêtre de contrôle dans sa durée maximale.
Timeout, perte de preuve ou opération non finie restent UNKNOWN, avec
admission fermée, sans annoncer STOPPED. La persistance terminale après
épuisement du budget est indiquée non prouvée si nécessaire ; le
superviseur reste propriétaire de la fin physique du processus.

reconcile_quiescence exige la vérification propriétaire de processus
disparu, effets réconciliés et réadmission actuelle, avec preuve fraîche
liée au slot et à son epoch. Les nombres d'effets actifs et inconnus
doivent être exactement nuls. Sans cette preuve, UNKNOWN ne se réactive
pas. La résolution passe par DRAINING puis STOPPED et ne relance aucun
handler.

Les recettes utilisent PostgreSQL 16.14, Django 6.1.2 et Python 3.14.9.
C04/C05/C06, Core, ASGI et lifecycle C07 sont réels dans les cas
correspondants. Les faits C03, sources N05/C08, ports C10 et observations
de supervision des fixtures sont explicitement synthétiques : ils ne
qualifient pas ces composants. Les pertes d'acquittement injectées après
vrai commit sont des simulations annoncées. Les SIGTERM ciblent
uniquement les enfants de test.

## Revue de livraison C09 du 23 octobre 2026

La réalisation ci-dessus est éprouvée localement dans le RUN
cismp2-pixs-432a76eb96094b9e. Les mentions de préparation des premières
sections conservent leur sens historique. La validation porte sur le profil
C09 et ses raccordements explicitement testés, sans qualification globale P0.

### Périmètre et preuves exécutées

Les 45 fichiers Python identifiés au checkpoint couvrent les modules backend
c09_*, leurs deux migrations, les deux participants Core c09_*, les fixtures
et les recettes C09. Dans le fichier partagé backend/models.py, C09 ajoute
seulement l'enregistrement de ses modèles ; les structures JobRecord et Bulk
préexistantes sont préservées. Aucun contrat public Core, manifeste de
composant, fichier frontend ou configuration OpenCode n'est modifié par ce RUN.
Les quatre canons events/interactions/jobs/runtime conservent leurs SHA-256
de requirements.md. Aucun delta normatif, dépendance, déploiement ou opération
Git, y compris en lecture, n'a été exécuté.

| Contrôle | Résultat observé | Référence native OpenCode |
|---|---|---|
| Compilation de l'ensemble C09 et recette locale complète | 45 fichiers compilés, 120 unités C09 et 15 recettes PostgreSQL couvrant 222 cas ; nettoyage et fermeture des connexions confirmés | call_01a166d1aa2772e7b7062cd4054d63df |
| Consolidation 2.4 | Six recettes PostgreSQL, 76 cas, tous réussis ; deux schedulers réellement multiprocessus et signaux aux seuls enfants de test | call_01a166dfc917724dad29c6162768706f |
| Non-régression applicable 3.1 | 946 tests dans 71 modules, zéro échec, erreur ou test sauté ; 45 compilations | call_01a166e36b3475628a95335649ec81fe |
| Isolation et intégrité 3.2 | 45 sources inchangées, 48 fichiers UTF-8/LF sans BOM, quatre canons inchangés, contrôle des 17 modules produits sans motif sensible ni accès fichier/secret ajouté | call_01a166e5c0bb71abbe81f962aabacc84 |
| OpenSpec strict C09 | Succès ; skip_specs reconnu, aucun delta requis | call_01a166dea7ad76cebb3ef99c39474a0b |

Les 946 unités incluent les 120 unités C09 ; les 76 cas de consolidation
réexécutent un sous-ensemble des 222 cas PG. Ces effectifs ne sont pas
additionnés comme des scénarios distincts. Environnement réellement observé :
Python 3.14.9, Django 6.1.2 et PostgreSQL 16.14. Aucune réussite sur une autre
version Python ou un autre moteur de base n'est déduite de ces résultats.

Le premier lancement élargi a échoué (920 tests, quatre échecs et trois erreurs,
call_01a166e1df937505848363ccff984aec). Les chemins src/tests/unit manquaient
dans la commande et dans l'environnement hérité de certains sous-processus ;
le lancement a été corrigé sans modifier les sources. Une assertion du test
historique TestManifests.test_schema_types_versions suppose encore un Core
sans capacités ni contrats. Elle est explicitement non applicable au Core C06
actuel : les cinq capacités, quinze contrats et vingt entrées sont vérifiés
par test_core_service_manifest, inclus dans les 946 tests. L'ancienne assertion
n'est ni déclarée réussie ni modifiée par C09 ; son échec initial reste conservé.

### Correspondance des scénarios et conditions

| Clauses de requirements.md | Preuves applicables et limites |
|---|---|
| events 8–63 ; interactions 18/36 | Contrats fermés versionnés, domaine/intégration distincts ; outbox invisible avant commit, rollback intégral sans trou de séquence, réception idempotente propre au consumer, ordre par partition, ACK après receipt durable. Recettes outbox20/inbox23/CoreInbox17 et unités de valeurs. |
| interactions 8 ; jobs 8/22/40 | Droits C04 et contexte N05 recontrôlés ; révocation avant/après effet refusée, audit C05 transactionnel. Sept cas Super Admin : waiver explicite courant et non hérité, retrait du grant et identité suspendue refusés. |
| interactions 27 | Aucun service Query métier ajouté/modifié ; polling technique borné distinct d'une mutation métier, contrats Query Core actuels préservés. |
| jobs 31/49 et 58–81 | États, checkpoints, déduplication propre C09, contexte et corrélation persistants ; 18 cas worker et 13 résilience. JobDeduplicationReferenceV1 reste un profil structurel distinct de l'idempotence durable. |
| events72 ; interactions45 ; jobs90/104 | B08/B09/B10/B11 Bulk conditionnels non sélectionnés ; aucun import de tables privées Bulk ni généralisation de leur bail. Aucune qualification Bulk supplémentaire revendiquée. |
| runtime42–116 | 28 unités de plan et 21 cas PG runtime : cumuls de budgets, sources demandées/accordées/appliquées distinctes, refus absent/partiel, reconfiguration quiescente, epochs et capacités bornés. Aucune mesure physique de performance du profil cible revendiquée. |
| runtime130/139/151/160 | 12 cas entrée process et 13 web ASGI : NORMAL courant, hooks réels C07, worker/scheduler sans ASGI, surfaces gardées et readiness refusée si prérequis absent. Aucune ouverture publique de socket de production. |
| runtime174/183 | 15 cas scheduler et 15 résilience : deux processus distincts, ancien détenteur expiré clôturé, rollback/reprise et doublons ; sept cas SIGTERM drainé ou UNKNOWN borné, jamais de faux STOPPED. |
| runtime23/192/205 | Frontières PBO/PA/PZT préservées et prérequis manquants fermés. Aucun provisioning, transport PA/PZT, mode distant/ZT ou recréation de conteneur PA/PZT sélectionné ou qualifié. |

### Impacts, migrations et limites finales

Les migrations 0012/0013 sont additives. Leur application, rejeu sans dérive
et retour sur schéma vide sont exécutés dans des schémas PG jetables. Le retour
sur données non vides est refusé et préserve les données ; aucun downgrade
automatique ni migration d'une base de production n'a été exécuté.
Le déploiement doit appliquer ces migrations et fournir les sources serveur
NORMAL/N05, budget effectif et ressources appliquées réellement vérifiables
avant readiness. Les DTO ou références opaques ne sont pas des autorisations.

Les recettes réutilisent réellement les contrats C04/C05/C06 et les hooks C07.
Les faits C03/N05, certains adaptateurs de cycle de vie et les observations
PBO sont des doubles nommés : ils démontrent les obligations de ports et leurs
refus, sans livrer C08, N05, C10 ni un exécutant PBO de distribution. Les effets
externes non transactionnels restent refusés. L'idempotence et l'ordre locaux
ne constituent aucune promesse exactly-once d'un transport externe.
Un traitement dont la fin n'est pas prouvée demeure UNKNOWN ; sa réadmission
exige les preuves serveur d'absence du processus et de réconciliation des
effets décrites plus haut.

Les contrôles npm, build frontend et navigateurs sont sans objet pour ce RUN :
aucun fichier frontend modifié ; l'entrée Django ASGI est réellement éprouvée.
Aucun lint ou vérificateur de types n'est configuré pour ce périmètre.
La qualification des profils physiques, du paquet et de son identité de
distribution reste à C17/C18/C19. Les autres changes et services partagés
restent sous leur propre pilotage.
