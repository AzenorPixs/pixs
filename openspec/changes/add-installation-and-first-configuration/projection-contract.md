# Projection technique PostgreSQL C08 vers PA01

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Cible consolidée du 31 octobre 2026 — ACL-PIXS-2026-10-31-E3-R1

Installation pré-domaine, amorçage technique distinct puis transition Domaine raccordée à C97/C96 ; le transfert ne réactive pas les anciennes identités.

Les orientations du modèle validé remplacent précisément les formulations antérieures incompatibles avec ce périmètre. Les autres clauses restent applicables. Les sections antérieures et leurs références sont conservées pour traçabilité ; elles ne doivent pas être utilisées pour réintroduire une décision remplacée. Les preuves et cases cochées ne qualifient que leur version d'origine.

### Sources et responsabilités courantes

- [installation-provisioning](../../specs/installation-provisioning/spec.md).
- [initial-administration](../../specs/initial-administration/spec.md).
- [pixs-instance](../../specs/pixs-instance/spec.md).
- [zt-pki](../../specs/zt-pki/spec.md).

Le canon courant prévaut sur ses copies de préparation. Le périmètre présent est documentaire : aucun code, test produit, migration, service, secret, publication ou Git n'est exécuté. Les choix de fournisseurs manquants restent à qualifier avant réalisation.

### Refus et critères de réalisation

Les scénarios des sources et de requirements.md doivent être reliés à des résultats vérifiables par unité. Réception n'est pas application ; donnée ancienne n'est pas état courant. Une autorisation expirée/révoquée ou une dépendance requise non qualifiée bloque l'usage concerné. La validation documentaire ne fait pas réussir les recettes futures.

### Préservation de l'historique et articulation des travaux

Les titres, codes, identifiants de tâches et de sous-lots, libellés, cases, statistiques et preuves antérieurs sont conservés. Les compléments sont rattachés aux unités existantes sans renumérotation ni validation produit anticipée. Les ouvertures C95/C96/C97/N08/PA12/Z28/Z29/Z30/Z31/Z32 portent leurs seules parts résiduelles ; elles ne relancent pas les archives.
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

Version de conception : 1.0.0. Propriétaire de l'intention et de la confirmation :
C08. Propriétaire du plan technique, des profils/résolveurs, de l'admission, du
registre et des effets : PA01/pixs.agent. Ce contrat précise les garanties déjà
adoptées et E4 ; il ne constitue ni API HTTP supplémentaire ni runtime qualifié.

## Capacités PA01 actuellement sélectionnées

Le contrat propriétaire PA01 courant conserve les données et sélectionne
Debian 13 x86_64 sur hôte physique ou VM. Les intentions C08 ne lui confèrent
aucune capacité supplémentaire. RECREATE et DATABASE_DROP sont indisponibles :
PA01 refuse le plan entier avant tout effet, sans les convertir en CREATE ni
exécuter un préfixe du plan. Leur réalisation exigerait un lot normatif PA
distinct explicitement validé par le développeur.

Le profil Docker de C08 demeure adopté comme cible de réalisation ; il n'est
pas sélectionné ni qualifié par PA01 courant. INITIALIZE_START et toute
projection de ce profil sont donc refusés par cette composition. Cette limite
ne réduit pas les exigences Docker de C08 et ne permet pas sa clôture sans
leurs réalisations et preuves requises.

## Frontières

Le PBO présente une intention technique avant l'acte R01. Il n'a pas besoin
d'un plan R01 déjà complet pour demander la préparation de sa connexion.
La projection exclut identité/tenant/credential applicatifs, preuve privée R01,
secret PostgreSQL, clé, SQL, shell et code. Les identifiants de connexion réels
restent dans les sources privées des résolveurs propriétaires.

PA inspecte service/rôle/base et produit ses observations protégées. C08 lie
l'intention à ces observations. PA dérive ensuite son TechnicalPlan fermé et
versionné, puis l'opérateur confirme explicitement les digests et les effets.
La projection ne contient ni digest du futur plan PA, ni confirmation, ni
signature, ni son propre digest. La référence de confirmation du plan PA peut
être allouée avant cette confirmation ; elle n'accorde aucun droit.

## Document fermé de projection

Tous les champs ci-dessous sont obligatoires. Les références et versions sont
des chaînes non vides bornées par la configuration protégée ; aucune référence
ne peut être interprétée comme chemin libre, SQL ou programme à exécuter.
La seule valeur nullable est causation_id. Aucune clé supplémentaire n'est
admise, y compris dans les objets imbriqués.

| Champ racine | Type et sens |
| --- | --- |
| schema_version | chaîne exacte 1.0.0 |
| projection_ref | référence opaque de cette publication immuable C08 |
| catalog_operation | chaîne exacte prepare_postgresql |
| catalog_version | chaîne exacte 1.0.0, comparée au catalogue livré PA |
| operation_id | identité de l'opération de préparation, distincte de l'inspection |
| installation_ref, target_ref | installation et hôte/VM/conteneur ciblés explicitement |
| runtime_profile_ref, runtime_profile_version | profil adopté, résolu par le serveur et comparé à la plateforme réelle |
| service | objet fermé ref, action, profile_ref, profile_version |
| role | objet fermé ref, action, profile_ref, profile_version, credential_binding_ref, credential_binding_version |
| database | objet fermé ref, action, profile_ref, profile_version |
| observation | objet fermé ref, version, sha256, issu de l'inspection propriétaire PA |
| allowed_effects | tableau ordonné sans doublon des seuls effets techniques ci-dessous ; peut être vide pour réutilisation intégrale |
| correlation_id, idempotency_key | chaînes non vides propres à cette préparation |
| causation_id | chaîne non vide ou null ; aucune identité ni permission déduite |
| correlation_ids, causation_ids | tableaux A07 complets recopiés de l’invocation : ordre et doublons conservés, jamais remplacés par les identifiants scalaires |

Le digest observation.sha256 est le SHA-256 hexadécimal minuscule de 64 caractères
du manifeste d'observation versionné propriétaire PA, résolu localement. Ce
manifeste lie installation/cible, service/rôle/base, profil courant, états,
versions et préconditions vérifiables. La référence seule ne vaut pas observation.
Sa fraîcheur et ses préconditions sont recontrôlées par PA avant chaque effet ;
le format exact du manifeste et sa production restent à figer par PA01.

## Actions et effets désirés

Les actions sont des intentions explicites, pas des correctifs conditionnels
choisis silencieusement par PA. Une observation divergente bloque ou conduit à
une réconciliation documentée d'un effet antérieur connu de cette même opération.

| Objet/action | Sémantique et seuls effets admissibles |
| --- | --- |
| service / INSTALL_CONFIGURE_START | Hôte physique/VM seulement : installer le logiciel prévu par le profil, configurer le service ciblé, initialiser le seul cluster absent explicitement visé si nécessaire, puis démarrer. SERVICE_INSTALL, SERVICE_CONFIGURE, SERVICE_START ; CLUSTER_INITIALIZE seulement si son absence est prouvée et cet effet est explicitement inscrit. |
| service / INITIALIZE_START | Indisponible dans PA01 courant ; refus du plan entier avant effet. Intention du profil Docker C08 à réaliser : utiliser le logiciel déjà fourni par l'image, initialiser le seul stockage PostgreSQL absent prévu par le profil, démarrer. SERVICE_START ; CLUSTER_INITIALIZE seulement si absent et explicitement inscrit. Aucun téléchargement/installation ou remplacement du stockage existant. |
| service / START_EXISTING | Démarrer un service/cluster existant conforme au profil courant. SERVICE_START seul ; aucune installation, réinitialisation ou reconfiguration. |
| service / REUSE_RUNNING | Vérifier et conserver le service existant conforme et actif. Aucun effet de service. |
| role / CREATE | Créer le seul rôle absent désigné, avec les attributs et la liaison de credential du profil protégé. ROLE_CREATE seul. Aucun rôle supplémentaire ni privilège de préparation transmis au rôle applicatif. |
| role / REUSE | Vérifier et conserver le rôle conforme avec sa liaison courante. Aucun effet de rôle ; aucune rotation/reset/ALTER ou suppression implicite. |
| database / CREATE | Créer la seule base absente désignée, avec propriétaire et paramètres du profil protégé. DATABASE_CREATE seul. |
| database / REUSE | Vérifier et conserver la base technique conforme. Aucun effet de base ; une migration de schéma applicatif éventuelle reste entièrement au PBO. |
| database / RECREATE | Indisponible dans PA01 courant ; refus du plan entier avant effet. Intention future exigeant un lot normatif PA distinct : recréer cette seule base incompatible sous les confirmations explicites distinctes exigées ci-dessous. DATABASE_DROP puis DATABASE_CREATE. Aucun cluster ni rôle supprimé, aucune autre base touchée. |

L'ordre canonique des effets est SERVICE_INSTALL, SERVICE_CONFIGURE,
CLUSTER_INITIALIZE, SERVICE_START, ROLE_CREATE, DATABASE_DROP, DATABASE_CREATE.
DATABASE_DROP reste exclu du catalogue admissible PA01 courant ; sa présence
bloque tout le plan avant effet. L'ensemble doit correspondre exactement aux actions choisies, aux observations
et au profil. Un effet absent, supplémentaire ou incompatible est refusé.
CLUSTER_INITIALIZE ne peut accompagner START_EXISTING ou REUSE_RUNNING.
RECREATE ne peut réinitialiser un cluster, réutiliser un mandat consommé ou
ouvrir une compensation destructive après issue inconnue. Les connexions actives
incompatibles bloquent RECREATE ; aucune interruption forcée ni extension
silencieuse du périmètre de service n'est autorisée par ces deux effets.

Les profils service/rôle/base sont fermés et versionnés sous propriétaire PA.
Ils doivent fournir tous leurs paramètres réels : logiciel/version/provenance,
unité et stockage concernés, accès SQL local peer/requirepeer déjà retenu,
identifiants SQL et attributs du rôle, liaison privée/version de credential,
propriétaire et paramètres de création/conformité de la base. Ils ne contiennent
aucun champ de SQL/shell libre. Leurs schémas exacts et leurs résolveurs natifs
restent à arrêter par PA01 avant handlers ; aucune valeur réelle n'est inventée
ici. PA obtient une valeur sensible par le seul canal privé explicitement
autorisé pour son identité/politique ; C08 et PZT ne la transportent jamais.
L'absence de ce canal ou de son audit bloque l'effet concerné.

## Confirmation et admission E4

La publication de projection ne donne aucun pouvoir. La confirmation opérateur
et le mandat E4 doivent lier cette publication et son digest, le plan PA et son
digest, installation/cible/opération/version, acteurs natifs/exécutant/relation
PZT, politique courante, préconditions et ensemble exact d'effets.

La référence de confirmation se résout vers un contenu protégé et immuable.
Pour une réalisation future préalablement adoptée, RECREATE exigerait la
confirmation du plan courant et une confirmation destructive
distincte, fraîche et liée à la même base, au même plan et à la projection.
Ces confirmations ne rendent pas admissible une capacité absente du PA courant.
Le mandat signé lie le bundle complet et son digest ; une simple liste de refs
ou un acquittement mémoire n'atteste pas ces consentements. Le schéma de confirmation PostgreSQL ci-dessous est maintenant fermé ; son stockage et son résolveur protégés restent à réaliser. Aucun bundle ni destruction supplémentaire n'est adopté silencieusement.
Un changement invalide les confirmations. Aucun reset du credential du futur
Super Admin ou acte Core/Auth n'entre dans cette confirmation technique.

La branche initiale ne se rouvre pas depuis un marqueur/base/fichier absent.
Après adoption/retrait des autorités initiales, un état installé ou restauré ne
peut demander RECREATE par une ancienne autorité d'amorçage. Les opérations
ordinaires gardent leurs propres autorités actuelles. Le registre/ancrage PA,
l'audit, la validité/révocation et les refus E4 restent obligatoires.

## Sérialisation et rapprochement avec le plan PA

JSON UTF-8, clés triées, séparateurs compacts, types stricts, doublons, champs
inconnus et constantes non finies refusés. Le tableau allowed_effects conserve l'ordre
canonique défini et son unicité. Les tableaux A07 correlation_ids et causation_ids
conservent intégralement l'ordre et les doublons reçus ; aucun tri, dédoublonnage
ou remplacement par les scalaires n'est admis. Aucune coercition. SHA-256 porte sur ces seuls octets.
Tailles/nombres/longueurs sont obligatoirement bornés par configuration protégée,
sans reprendre des valeurs de fixtures comme défauts de production.

Les service.ref, role.ref et database.ref correspondent exactement aux
service_ref, role_ref et database_ref du TechnicalPlan PA. Celui-ci lie aussi
projection_ref, confirmation_ref, policy_ref, preconditions_ref, installation,
cible, opération/version, corrélation et idempotence selon son contrat propre.
La résolution de projection_ref doit donner les octets immuables confirmés,
pas un dictionnaire fourni librement par un client. Le contrôle PA compare la
sémantique des actions, effets, profils et observations, sans se limiter à un
digest de trois références. Les invariants se recontrôlent après attente/reprise.

Le résultat technique reste le NativeResult propriétaire PA. Un état durable
réconcilié service/rôle/base ne prouve ni connexion PBO, migration applicative,
acte R01, commit Core/Auth/C05/C08 ou disponibilité. Le raccord conservera
les corrélations scalaires, les tableaux A07 complets dans leur ordre avec leurs
doublons, et les preuves durables de chaque propriétaire.

## Vérifications à préparer, non exécutées

Refuser action/effet inconnu, rôle cible substitué, profil/version absent,
observation périmée ou d'une autre cible, tentative d'installation Docker,
stockage présent réinitialisé, confirmation destructive absente/ancienne,
paramètre de secret/SQL/code ajouté, signature ou politique non courante,
rejeu divergent, ancien état restauré et issue d'effet inconnue.
Comparer les octets/digests et objets résolus, puis qualifier les effets réels
sur les seuls environnements autorisés. Cette conception n'exécute aucun test,
SQL, installation ou effet TPM/NV et n'ajoute aucune tâche cochée.

## Transcription E5 adoptée documentairement, non réalisée ni qualifiée

Cette projection 1.0.0 conserve la Projection, NativeRequest, TechnicalPlan, NativeResult et le catalogue trois opérations 1.0.0. Elle ne redéfinit ni le wire, ni les manifestes, ni les résolveurs, qui restent propriétaires PA01.

Le profil d'échange 1.1 est distinct des contrats 1.0. La requête porte schema pixs.agent.postgresql.exchange.request, schema_version 1.1.0, purpose et request, où request est le NativeRequest 1.0.0 inchangé. Les purposes exacts sont OBSERVE vers inspect_postgresql sans champ supplémentaire, PREPARE_PLAN vers inspect_postgresql avec projection_document, projection_binding et confirmation_ref préallouée, PREPARE vers prepare_postgresql sans champ supplémentaire, READ_RESULT vers get_postgresql_result sans champ supplémentaire. La réponse porte schema pixs.agent.postgresql.exchange.response, schema_version 1.1.0, purpose, result issu de NativeResult 1.0.0 et payload, vide hors SUCCEEDED, contenant en SUCCEEDED pour OBSERVE observation_document et observation_binding, pour PREPARE_PLAN planning_bundle et planning_binding, et objet vide pour PREPARE et READ_RESULT.

Le mandat initial 1.1 conserve le domaine PA_POSTGRESQL_INITIAL et les champs E4, avec schema_version 1.1.0, catalog_version 1.0.0 et préfixe signé PIXS:PA:POSTGRESQL:INITIAL:1.1.0 suivi de LF. Son request_digest engage tous les octets canoniques de l'enveloppe 1.1 entière, jamais la seule requête interne. PA retourne l'observation puis le planning avant toute confirmation C08. C08 lie son intention à l'observation vérifiée, puis confirme le plan, les préconditions et les effets avant l'acte signé.

L'observation 1.0.0 porte les cinq ressources uniques ordonnées SOFTWARE, CLUSTER, SERVICE, ROLE, DATABASE, chacune avec kind, resource_ref, state, match et evidence_binding de sources protégées. UNOBSERVABLE n'est jamais ABSENT et impose UNDETERMINED sans devenir une absence. L'observation initiale est immuable et réutilisée après vérification propriétaire. Les préconditions 1.0.0 sont stagiées avec resource_guards complets pour les cinq ressources même en REUSE ou effets vides : les contrôles rôle et base après démarrage du service et avant leurs effets, conditions BEFORE_EFFECT ou AFTER_SERVICE_START_BEFORE_EFFECT, preuve actuelle d'ABSENT obligatoire avant chaque CREATE après SERVICE_START, et conformité complète avant SUCCEEDED. Aucune conversion silencieuse de CREATE en REUSE ni compensation destructive.

Le manifeste d'effets lie l'ensemble du document par effects_binding, tandis que effects_digest reste le SHA-256 du seul tableau canonique allowed_effects ordonné. Ces deux empreintes ne sont pas confondues. Docker, INITIALIZE_START, RECREATE et DATABASE_DROP restent refusés par le PA sélectionné avant tout effet, sans conversion ni adoption silencieuse.

La confirmation C08 fermée utilise schema pixs.c08.postgresql-confirmation.v1, schema_version 1.0.0, avec exactement les seize champs suivants :

| Champ | Type strict et correspondance |
| --- | --- |
| schema | chaîne exacte pixs.c08.postgresql-confirmation.v1 |
| schema_version | chaîne exacte 1.0.0 |
| confirmation_ref | chaîne non vide stricte bornée par le profil protégé, référence opaque C08 respectant le format exact existant y compris UUID si imposé, correspond à TechnicalPlan.confirmation_ref préallouée, propriétaire C08 |
| installation_ref | chaîne non vide stricte bornée par le profil protégé, respectant le format exact existant y compris UUID si imposé, correspond à l'installation commune de la projection et du plan, rapprochée par PA et C08 |
| target_ref | chaîne non vide stricte bornée par le profil protégé, respectant le format exact existant y compris UUID si imposé, correspond à la cible commune de la projection et du plan |
| operation_id | chaîne non vide stricte bornée par le profil protégé respectant le domaine propriétaire courant sans format incompatible inventé, identité de la préparation future distincte des lectures, correspond à TechnicalPlan.operation_id |
| operator_ref | chaîne non vide stricte bornée par le profil protégé respectant le domaine propriétaire courant sans format incompatible inventé, référence de l'opérateur, correspond au mandat critique 1.1, propriétaire C08 |
| projection_binding | ContentBinding exact avec ref chaîne non vide bornée, version chaîne non vide bornée valant 1.0.0, sha256 hexadécimal minuscule 64 caractères, sans coercition ni type nullable implicite, engage la publication C08 immuable |
| observation_binding | ContentBinding exact avec ref chaîne non vide bornée, version chaîne non vide bornée valant 1.0.0, sha256 hexadécimal minuscule 64 caractères, sans coercition ni type nullable implicite, engage le manifeste d'observation PA |
| plan_binding | ContentBinding exact avec ref chaîne non vide bornée, version chaîne non vide bornée égale à plan_version opaque existante sans valeur inventée, sha256 hexadécimal minuscule 64 caractères, sans coercition ni type nullable implicite, engage TechnicalPlan 1.0.0 |
| preconditions_binding | ContentBinding exact avec ref chaîne non vide bornée, version chaîne non vide bornée valant 1.0.0, sha256 hexadécimal minuscule 64 caractères, sans coercition ni type nullable implicite, engage le manifeste de préconditions PA |
| effects_binding | ContentBinding exact avec ref chaîne non vide bornée, version chaîne non vide bornée valant 1.0.0, sha256 hexadécimal minuscule 64 caractères, sans coercition ni type nullable implicite, engage le manifeste d'effets entier |
| policy_ref | chaîne non vide stricte bornée par le profil protégé, référence de politique courante, correspond au mandat, propriétaire PA |
| policy_version | chaîne non vide stricte bornée par le profil protégé, version de politique courante, correspond au mandat |
| confirmed_at | chaîne non vide stricte, UTC YYYY-MM-DDTHH:MM:SS.ffffffZ, six chiffres exacts, sans conversion |
| correlation_id | chaîne non vide de la préparation, ne remplace aucun tableau A07 |

Chaque ContentBinding possède exactement ref, version et sha256, avec sha256 hexadécimal minuscule de 64 caractères des octets canoniques du document lié. L'acyclicité exclut tout digest du plan futur ou de la confirmation dans la projection, tout digest du futur bundle dans le plan, et tout acte, signature ou digest de futur mandat dans la confirmation. Les comparaisons de cible, installation, opération, politique et références lient la projection, le plan, les préconditions, les effets et la confirmation sans les confondre. Cette confirmation est distincte de la future confirmation administrative de retrait PA du domaine PA_POSTGRESQL_WITHDRAWAL. Elle ne porte ni tableaux A07 futurs, ni signature, ni digest de futur mandat. Les structures des manifestes, les profils et les octets canoniques restent définis par PA01 ; cette projection s'y réfère sans les redéfinir.

### Documents imbriqués 1.1 E5 — objets JSON canoniques

Pour le seul profil 1.1 E5, projection_document, observation_document, plan_document, preconditions_document, effects_document et planning_bundle sont des objets JSON imbriqués fermés, jamais des chaînes. request et result restent les objets NativeRequest/NativeResult 1.0.0 inchangés. Cette représentation wire 1.1 en objets imbriqués est distincte des types INCHANGÉS de chaque API propriétaire 1.0 ; côté C08, dump_projection_canonical produit bytes ; parse_projection_bytes accepte bytes et vérifie l'égalité de re-sérialisation, sans coercition str/bytes.

Chaque document est hashé depuis ses propres octets canoniques UTF-8, clés triées, séparateurs compacts, types stricts, sans champ inconnu, sans clés JSON dupliquées, sans constante non JSON ; les tableaux A07 conservent ordre et doublons, sans dédoublonnage des valeurs, revalidé par son codec propriétaire et ses bornes protégées. Aucun hash ne porte sur le JSON échappé d'une chaîne. planning_binding.sha256 lie SEULEMENT le bundle entier ; request_digest du mandat 1.1 lie SÉPARÉMENT l'enveloppe requête 1.1 entière ; effects_binding.sha256 lie le manifeste entier, effects_digest seulement allowed_effects.
