# PA/PZT — Détail validé du stockage S1, du relais R1 et des fournisseurs F1

Date : 27 octobre 2026.

## 1. Statut, décisions acquises et adoption des détails

**D-S1, D-R1, D-F1 ET D-SMIG VALIDÉS PAR LE DÉVELOPPEUR — DOCUMENTATION UNIQUEMENT.**
Aucune implémentation, production de code, migration ou recette produit.

Source du 27 octobre 2026 : « Je valide les propositions D-S1, D-R1, D-F1
et D-SMIG. Inscris ces décisions dans les spécifications et le cadrage PA/PZT,
sans implémentation ni production de code, en distinguant les choix validés
des réalisations et preuves manquantes. »

Les orientations [S1/R1/F1](DECISIONS_S1_R1_F1.md) sont validées et canoniques :
tables PostgreSQL privées Agent, outbox transactionnelle avec relais PBO
vers PZT, fournisseurs propriétaires par responsabilité. Les détails
[D-A1/D-A2/D-A3/D-MIG](DETAIL_A1_A2_A3.md) restent acquis.
Les noms, schémas, contraintes, contrats privés et règles de migration
ci-dessous sont désormais ADOPTÉS DOCUMENTAIREMENT.

| Décision validée | Détail adopté | Réalisation et preuves encore manquantes |
| --- | --- | --- |
| D-S1 | Huit tables privées, colonnes, clés, contraintes, index et règles d'accès. | Modèles, dépôts, DDL/migrations, contrôles d'intégrité et preuves PostgreSQL réelles. |
| D-R1 | Interface privée du relais, réservation, tentatives, transitions et réconciliation. | Relais et hébergement PBO, intégration transactionnelle/transport, reprise et garanties natives éprouvées. |
| D-F1 | Interfaces privées nommées, entrées/sorties, fournisseurs et composition. | Implémentations exécutables et versions, composition authentique, gardes, résolution, origine et confirmation qualifiées. |
| D-SMIG | Application physique de M0–M5, classification, bascule et retour/restauration. | Graphe et migrations exécutables, environnement autorisé, compatibilité et preuves de conservation/restauration. |

Ces nouvelles exigences sont inscrites dans les deltas PA01
[pixs-agent](specs/pixs-agent/spec.md) et [pzt](specs/pzt/spec.md).
Elles restent NON SYNCHRONISÉES au canon par cette inscription ; les
synchronisations et décisions canoniques antérieures sont conservées.
Aucun nouveau contrat public, champ wire PA/PZT, endpoint, port, compte
système, durée, plafond opérationnel, dépendance ou autorité n'est sélectionné.
Les versions privées validées 1.0.0 ci-dessous ne changent ni
AgentPaBinding 1.0.0, ni Agent 2.0.0, ni les versions E4/E5.

Sources courantes : [modèles Agent](../../../src/pixs/agent/models.py),
[dépôt](../../../src/pixs/agent/repository.py),
[identifiants et codecs](../../../src/pixs/agent/identifiers.py),
[service](../../../src/pixs/agent/service.py),
[ports Agent](../../../src/pixs/agent/ports.py),
[ports PZT](../../../src/pixs/pzt/ports.py),
[contrat de temps](../../../src/pixs/kernel/contracts/time.py),
[contrats PA01](contracts.md),
[raccord du temps](../add-pzt-ca-hierarchy-rotation-and-recovery/RACCORDS_TEMPS_V2.md).

## 2. Contraintes de départ observées

| Constat vérifié dans les sources | Conséquence retenue |
| --- | --- |
| AgentHead, AgentOperation et AgentFact possèdent déjà des UUIDv7, scopes, générations et données canoniques. | Référencer ces identités ; ne pas recopier ou renuméroter les opérations/faits. |
| Le dépôt peut rejoindre une transaction englobante ; la durabilité intervient au commit le plus externe. Le service possède ses frontières durables propres. | R1 exige l'observation du commit propriétaire final ; le retour d'une fonction du dépôt ou d'un savepoint ne suffit pas. |
| Le souhaité a déjà une unicité d'idempotence et de génération ; les traces ne participent pas au fingerprint métier. | Même domaine et comparaison intégrale après digest ; aucune seconde identité créée par le contrat temporel ou les traces d'un nouvel appel. |
| dispatch refuse PZT_TRANSPORT_UNAVAILABLE ; le lifecycle PZT refuse PZT_EXECUTION_UNAVAILABLE ; le contexte TLS indique ready_for_transport=False. | Aucun relais ni fournisseur de transport opérationnel n'est réputé livré. |
| Les ports de confiance Agent sont des Protocols ; le temps expose TimeProducer avec quatre méthodes. | Décrire les adaptateurs concrets futurs sans transformer un DTO, diagnostic ou retour None en permission persistante. |
| Les dates contractuelles sont du texte ; BaseAgent.version est un compteur entier. | Conserver les textes exacts et séparer version du payload et version technique de stockage. |

## 3. D-S1 — Schéma physique validé

### 3.1 Règles communes

Huit tables dans l'application Django pixs_agent et la même base PostgreSQL
que les états Agent. Les noms validés sont privés, sans nouveau schéma SQL
ou base séparée. Aucun DDL ou fichier de migration n'est fourni.

UUID désigne un identifiant serveur UUIDv7 selon le validateur existant ;
il n'est ni une identité d'acteur ni une horloge d'autorité. TEXT désigne
un texte UTF-8 non vide, sans NUL, borné par le profil applicable, sauf
nullable explicitement. HEX64 désigne TEXT limité à 64 caractères
hexadécimaux minuscules. Les références opaques restent TEXT ; elles ne
deviennent pas des UUID ou des clés étrangères vers une table d'un autre
propriétaire par ressemblance de forme.

BIGINT utilise les bornes int64 du stockage Agent : générations non négatives,
révisions et numéros de tentative positifs. Saturation : refus explicite,
jamais rebouclage. Les booléens sont refusés à l'entrée des contrats entiers.
Les champs temporels engagés restent TEXT avec leur grammaire contractuelle ;
TIMESTAMPTZ sert seulement au suivi local et à l'ordonnancement, pas à
remplacer les gardes temporelles au point d'usage.

Les métadonnées de gouvernance et de cycle des données suivent BaseAgent :
version entière, created_at/updated_at UTC, governance_ref, confidentiality,
personal, persistence_state et retention_state. Inconnu reste restrictif ;
aucune classification publique ou durée de conservation implicite.
Les écritures immuables ne changent pas updated_at après création.

### 3.2 Inventaire et responsabilités

| Table validée | Clé et rôle | Mutabilité |
| --- | --- | --- |
| pixs_agent_pa_binding | id UUID ; identité et payload de rapprochement D-A1. | Immuable. |
| pixs_agent_pa_binding_state | binding_id UUID, PK/FK vers binding ; révision et état courants. | Mise à jour contrôlée par révision attendue. |
| pixs_agent_pa_binding_revision | PK composée binding_id/revision ; historique de chaque état. | Ajout seulement. |
| pixs_agent_payload_document | id UUID ; octets exacts de documents possédés par Agent. | Ajout seulement. |
| pixs_agent_pa_outbox | id UUID ; intention de remise et état local du relais. | Identité immuable ; état/réservation sous contrôle de concurrence. |
| pixs_agent_pa_attempt | id UUID ; tentative liée à une réservation du relais. | Ajout seulement. |
| pixs_agent_pa_delivery_event | id UUID ; événements locaux et références des retours/résolutions. | Ajout seulement. |
| pixs_agent_payload_provenance | id UUID ; version, précision et provenance d'un ancien ou nouveau payload Agent. | Historique de classification par ajouts. |

Les clés étrangères locales protègent la suppression, sans cascade destructive.
Les colonnes de portée sont dans binding et les lignes qui ciblent directement
des opérations/faits ; les autres lignes héritent du périmètre par jointure
obligatoire à binding. Un identifiant seul ne suffit jamais à lire une ligne.

### 3.3 Binding immuable : colonnes et correspondance D-A1

Toutes les colonnes ci-dessous sont non nulles sauf indication contraire.
Les projections physiques supplémentaires ne deviennent pas des champs du
modèle logique fermé AgentPaBinding ou des messages PA.

| Colonnes physiques validées | Type et provenance |
| --- | --- |
| id, binding_schema_version | UUID ; TEXT exactement 1.0.0. id représente binding_ref via l'encodage serveur des références, sans accepter un UUID fourni comme autorité. |
| request_kind, agent_contract_version | TEXT : MUTATION/READ ; contrat Agent effectivement sélectionné. |
| operation_id, head_id | UUID FK vers AgentOperation et AgentHead ; nullables pour READ seulement selon le contexte réel. MUTATION exige les deux. |
| scope_type, tenant_id, scope_id | TEXT ; tenant_id/scope_id nullables selon la forme ScopeContext existante : PLATFORM sans tenant/scope, TENANT avec tenant et scope optionnel. |
| agent_target_id, actor_ref | TEXT ; cible et acteur issus du contexte serveur courant. |
| agent_request_operation_id | TEXT ; identifiant logique Agent, distinct de operation_id de stockage et de l'invocation native. |
| agent_catalog_operation, agent_catalog_version | TEXT ; projections de l'instruction Agent acceptée, distinctes du catalogue technique PA. |
| idempotency_key, identity_canonical, identity_digest | TEXT, TEXT, HEX64 ; domaine agent-idem.v1 existant, sans ajout de agent_contract_version au namespace. |
| expected_generation, bound_generation | BIGINT ; valeurs Agent vérifiées, sans conversion de compteur PA. MUTATION reprend exactement les valeurs de l'opération ; READ n'incrémente rien. |
| agent_request_digest, agent_content_document_id | HEX64 et UUID FK vers payload_document ; digest Agent et octets canoniques de contenu correspondants. |
| agent_trace_document_id | UUID FK vers payload_document ; traces Agent exactes conservées dans leur ordre, sans participation nouvelle au fingerprint métier. |
| native_protocol_profile, native_catalog_operation, native_catalog_version | TEXT ; profil et catalogue techniques fermés sélectionnés. |
| native_purpose, native_subject_operation_ref | TEXT nullables ; purpose selon E5, sujet selon READ_RESULT ; aucune valeur fabriquée en profil 1.0.0 ou hors lecture de résultat. |
| native_request_operation_id | TEXT ; invocation native distincte de l'opération lue. |
| installation_ref, native_target_ref, pzt_relation_ref, executor_terminal_ref | TEXT ; rapprochement par les propriétaires, sans identité calculée depuis le client. |
| native_request_ref, native_request_digest, trace_binding_ref | TEXT ; référence des octets natifs chez leur propriétaire, digest du profil natif et liaison des corrélations/causalités signées. Le digest n'est pas remplacé par celui du document Agent. |
| accepted_at, authority_context_ref, time_evidence_ref | TEXT ; instant UTC à six décimales de l'acceptation et références historiques D-A1. Les gardes futures sont tracées séparément. |

Une lecture sans tête/opération souhaitée ne crée pas de tête ni génération
artificielle : bound_generation doit être résolue par la source Agent
compétente ; à défaut le raccord de gestion ordinaire est bloqué. Le parcours
initial avant PostgreSQL reste chez C08/PA, hors de ces tables. Une lecture
ultérieure de son résultat conserve ce contexte initial sans lui attribuer
rétroactivement une opération Agent.

### 3.4 État courant, révisions et documents

| Table | Colonnes spécifiques validées | Intégrité attendue |
| --- | --- | --- |
| binding_state | binding_id UUID ; revision BIGINT ; state TEXT ; state_reason_ref TEXT nullable. | État PREPARED/ACTIVE/SUSPENDED/RETIRED ; couple binding_id/revision référencé dans binding_revision. Même état/raison que la révision pointée. |
| binding_revision | binding_id UUID FK ; revision BIGINT ; previous_revision BIGINT nullable ; state TEXT ; state_reason_ref nullable ; changed_at TEXT UTC six décimales ; actor_context_ref, authority_check_ref, time_check_ref TEXT. | Première révision 1 sans précédente ; ensuite précédente = revision moins 1. Références de contrôles = traçabilité non réutilisable. |
| payload_document | id UUID ; document_kind TEXT ; payload_contract_version TEXT ; codec TEXT ; payload_bytes BYTEA ; byte_length BIGINT ; bytes_sha256 HEX64. | Types fermés AGENT_CONTENT/AGENT_TRACE/AGENT_OBSERVATION ; contenu non vide, longueur égale aux octets, empreinte vérifiée ; codec et version compatibles avec le type de document. |

Document Agent signifie contenu dont Agent possède déjà la persistance ;
aucun credential, clé, certificat ou copie nouvelle de preuve native n'entre
dans cette table. Les octets natifs restent chez leurs propriétaires.
Une éventuelle projection JSONB est reconstruisible à partir du document
validé et n'est pas source de signature, d'empreinte ou d'autorité.

Les codecs locaux validés sont fermés par type : AGENT_CONTENT réutilise
agent-content.v1 ou agent-content.v2 selon le contrat ; AGENT_TRACE emploie
agent-traces.v1, objet JSON aux trois clés exactes request_operation_id,
correlation_ids et causation_ids, encodage UTF-8 compact à clés triées,
sans LF ajouté, listes dans leur ordre et doublons conservés ;
AGENT_OBSERVATION emploie agent-observed-opaque.v1, octets UTF-8 exacts du
document Agent accepté sans parsing, normalisation ou resérialisation.
Ces deux derniers noms sont des décisions de stockage privé, pas de
nouveaux canons de signature ou domaines d'idempotence.

La révision et l'état courant sont écrits dans une même transaction sous
verrou de l'état, avec comparaison de la révision attendue. Le cycle D-A1
s'applique sans nouvelle transition. L'immutabilité est garantie par les
chemins d'écriture du dépôt et leurs contrôles ; un CHECK seul ne suffit
pas à empêcher la modification d'une ancienne ligne ou à vérifier une autre
table. Le rôle applicatif n'est pas réputé protéger contre un administrateur
de base hostile ; aucun nouveau compte ou privilège n'est configuré ici.

### 3.5 Intention, réservation, tentatives et événements

| Table | Colonnes spécifiques validées |
| --- | --- |
| pa_outbox | id UUID ; binding_id UUID FK unique ; expected_binding_revision BIGINT ; revision BIGINT ; state TEXT ; staged_owner_operation_id UUID nullable pour READ ; native_request_ref TEXT ; claim_epoch BIGINT ; claim_id UUID nullable ; worker_ref TEXT nullable ; claim_until TIMESTAMPTZ nullable ; next_attempt_at TIMESTAMPTZ nullable. |
| pa_attempt | id UUID ; outbox_id UUID FK ; attempt_no BIGINT ; claim_epoch BIGINT ; claim_id UUID ; binding_revision BIGINT ; composition_ref TEXT ; prepared_at TEXT UTC six décimales ; authority_check_ref et time_check_ref TEXT. |
| pa_delivery_event | id UUID ; attempt_id UUID FK ; event_no BIGINT ; event_kind TEXT ; occurred_at TEXT UTC six décimales ; recorded_at TIMESTAMPTZ ; detail_ref TEXT nullable ; transport_receipt_ref TEXT nullable ; native_operation_ref/native_result_ref/native_snapshot_ref/native_revision_ref/response_digest/origin_proof_ref/time_evidence_ref TEXT nullables selon l'événement ; postcondition_refs TEXT[] nullable hors OWNER_SNAPSHOT, références dans leur ordre propriétaire. |

L'intention désigne une seule demande logique native déjà liée. Sa référence
et son empreinte native ne changent pas entre tentatives ; une nouvelle
invocation impose le parcours d'autorisation et d'idempotence propriétaire.
staged_owner_operation_id reprend l'opération existante pour MUTATION ;
pour READ le contexte accepté est enregistré sans souhaité supplémentaire.

Un événement OWNER_SNAPSHOT porte toutes les références du reçu D-A1 §3.5,
y compris binding_ref obtenu par jointure et postcondition_refs ordonnées.
Un reçu incomplet ne devient pas un snapshot vérifié. Les octets de réponse
restent chez leur propriétaire ; les dates locales ne décident pas l'ordre
causal. Les callbacks tardifs restent traçables sur leur tentative sans
avancer la génération suivante.

PENDING impose next_attempt_at renseigné par le profil serveur ; les autres
états n'utilisent pas ce champ comme droit de remise. Les tableaux de
références sont unidimensionnels, sans élément nul ou vide et bornés par le
profil ; ordre et éventuels doublons propriétaires ne sont pas normalisés.

Genres validés d'événement : PREPARED, IO_STARTED, LOCAL_REFUSAL,
SUBMIT_ACK, SUBMIT_REFUSAL, TRANSPORT_UNKNOWN, OWNER_SNAPSHOT,
STALE_CALLBACK. Ce sont des états de suivi privés, pas les phases PA ou
les quatre issues Agent. Les corps bruts non vérifiés ne sont pas journalisés.

### 3.6 Provenance séparée

| Colonnes validées | Type et règle |
| --- | --- |
| id, operation_id, fact_id, document_id | UUID ; trois FK cibles nullables mais exactement une renseignée. |
| classification_revision, supersedes_id | BIGINT positif ; UUID FK nullable vers la classification précédente de la même cible ; première révision 1. |
| classification_state | TEXT : CLASSIFIED, AMBIGUOUS ou INVALID. |
| payload_contract_version, codec, source_precision | TEXT nullables seulement hors CLASSIFIED ; précision SECOND ou MICROSECOND selon la source réellement établie, NOT_APPLICABLE pour un document sans champ temporel. |
| producer_ref, writer_version, evidence_ref | TEXT nullables hors CLASSIFIED ; provenance inspectable du producteur et de son format d'écriture. |
| source_bytes_sha256, classified_at | HEX64 et TEXT UTC six décimales ; empreinte du contenu historique exact inventorié et date du classement. |

Une classification ultérieure ajoute une révision liée, sous verrou de la
cible ; elle ne remplace pas l'ancienne preuve. La version technique de
BaseAgent reste entière. L'empreinte calculée pour l'inventaire n'est pas
présentée comme un digest signé qui n'existait pas. La définition des octets
inventoriés est fixée par type de payload, sans sérialisation ad hoc d'un
ORM complet :

- AgentOperation : octets UTF-8 exacts de content_canonical, sans LF ajouté,
  avec son codec de contenu déjà sélectionné ; identité et métadonnées sont
  contrôlées séparément.
- AgentFact : codec d'inventaire privé validé agent-fact-inventory.v1 ;
  tableau JSON ordonné des valeurs id, operation_id, observed_fact_id,
  scope_type, tenant_id, scope_id, target_id, generation, kind, outcome,
  occurred_at, observed_at, origin_proof, observed_document, source_ref,
  proof_ref et postcondition_ref. UUID en texte canonique, entiers exacts,
  null conservé, chaînes sans transformation ; UTF-8 compact, Unicode
  conservé, sans flottant ni LF ajouté. Ce digest d'inventaire ne devient
  ni une signature ni une preuve de version du producteur.
- Document : payload_bytes exacts et codec déjà liés au document.

La présence d'un codec d'inventaire n'établit pas payload_contract_version :
le classement requiert toujours la provenance du producteur et la validation
du contrat correspondant. Les champs temporels d'un même payload doivent
être cohérents avec cette version ; un mélange reste ambigu ou invalide.

### 3.7 Contraintes, index et accès validés

| Repère de contrainte/index | Définition documentaire |
| --- | --- |
| binding_identity_uq | Unicité identity_digest ; après rapprochement, comparaison de identity_canonical et du contenu exact. Collision ou contenu divergent : refus, jamais seconde liaison. |
| binding_operation_uq | Unicité partielle operation_id pour MUTATION ; une opération souhaitée ne reçoit pas deux liaisons natives concurrentes par contournement. |
| binding_shape_ck | request_kind/profils/versions fermés, forme ScopeContext, nullabilité conditionnelle de operation_id/head_id/purpose/subject_operation_ref et bornes numériques. |
| binding_owner_fk | FK locales vers tête/opération/documents ; périmètre, acteur, catalogues, générations, contenu et appartenance des documents vérifiés sous verrous par le dépôt. Aucun CHECK prétendu intertables. |
| binding_revision_pk, binding_current_fk | Historique unique binding_id/revision ; pointeur courant vers révision existante, état/raison rapprochés dans la transaction. |
| outbox_binding_uq | Une intention par binding ; référence native identique à celle de binding. |
| outbox_claim_ck | Réservation complète claim_id/worker_ref/claim_until seulement en RESERVED ; claim_epoch monotone, révision attendue vérifiée. Hors RESERVED ces champs sont nuls, sans effacer les tentatives historiques. |
| attempt_number_uq, delivery_event_number_uq | Unicité outbox_id/attempt_no et attempt_id/event_no ; insertion concurrente divergente refusée. |
| provenance_target_ck, provenance_revision_uq | Exactement une cible ; trois unicités partielles cible/classification_revision, une par FK cible, et lien de succession cohérent. |
| binding_scope_idx | B-tree scope_type/tenant_id/scope_id/agent_target_id/bound_generation pour les lectures contrôlées. |
| outbox_pending_idx | B-tree next_attempt_at/id limité à PENDING ; outbox_reconcile_idx sur les intentions RECONCILE_REQUIRED. |
| attempt_history_idx, native_result_idx | Historique outbox_id/attempt_no ; recherche propriétaire native_operation_ref/native_revision_ref, sans considérer l'index comme preuve d'ordre. |

Les FK et contraintes structurelles sont contrôlées par PostgreSQL ; les
conditions de mandat, autorité, immutabilité métier et comparaison entre
propriétaires restent des contrôles de service au point d'usage.
Les contraintes uniques portant sur des valeurs optionnelles sont définies
par index partiels explicites, sans compter sur une égalité implicite entre NULL.
Le plan de déploiement précisera les noms SQL définitifs compatibles avec
les limites d'identifiants et les opérations de migration Django.

## 4. D-R1 — Contrat privé du relais validé

### 4.1 Frontières et entrées

Nom de contrat de composition validé : AgentRelay 1.0.0, privé PBO.
Le relais n'est ni un exécutant PA, ni une autorité unifiée, ni un cinquième
binaire. Sa forme d'hébergement PBO reste à sélectionner selon le lifecycle
existant, sans démarrage ou ordonnanceur ajouté par ce document.

| Opération privée validée | Entrée obligatoire | Sortie et garantie |
| --- | --- | --- |
| stage_submission | Transaction propriétaire courante, instruction/contexte acceptés, binding complet, références des documents et demande native préparée. | outbox_ref et révision ; résultat encore transactionnel, non présentable comme commit, remise ou permission. |
| observe_commit | outbox_ref, identité du propriétaire et des lignes attendues, alias serveur vers la même base primaire. | LocalCommitObservation avec références et révisions relues depuis une transaction indépendante ; absence, divergence ou doute bloquent l'envoi. |
| reserve_next | Identité serveur du worker, composition vérifiée, profil de tentative applicable. | RelayReservation : outbox_ref, binding_ref, claim_id, claim_epoch, outbox_revision, binding_revision et échéance locale ; aucune autorité distante. |
| prepare_attempt | Réservation courante, références acceptées, fournisseurs requis. | attempt_ref après gardes courantes ; aucun envoi. Échec de garde = refus tracé. |
| submit_attempt | attempt_ref et réservation encore courante ; demande native exacte résolue chez son propriétaire. | TransportObservation typée ; événement IO_STARTED persisté avant l'appel potentiellement émetteur. |
| record_observation | attempt_ref, réservation/révision attendues, observation du fournisseur transport. | Événement durable et nouvel état local, sans fait appliqué ou confirmé automatique. |
| reconcile_submission | outbox_ref, contexte courant de lecture, sources PZT/PA propriétaires. | Snapshot résolu ou incertitude conservée ; décision de remise ultérieure seulement après rapprochement et gardes. |
| pause_or_cancel | outbox_ref, révision attendue, motif propriétaire et preuve requise. | PAUSED ; CANCELLED uniquement si absence d'émission prouvée. Une intention émise ne disparaît pas par annulation locale. |

LocalCommitObservation est une donnée interne produite par le raccord de
transaction, pas un booléen d'appelant. La relecture vérifie ensemble
opération MUTATION éventuelle, binding, première révision et intention,
leurs identités et octets/digests attendus. Un alias inconnu ou une réplique
ne remplace pas la base primaire attendue. Un résultat de commit inconnu
reste inconnu jusqu'à résolution ; l'absence momentanée d'une ligne ne
constitue pas à elle seule une preuve de rollback.

### 4.2 Séquence et concurrence

1. Préparer et valider le contexte et la demande native auprès des propriétaires.
   La préparation n'émet pas vers PA et ne consomme pas de mandat critique.
   Si un propriétaire doit conserver les octets natifs avant le commit Agent,
   ce staging reste séparé : son éventuel orphelin ne vaut pas opération exécutée
   et sa réconciliation/nettoyage appartient à ce propriétaire.
2. Pour MUTATION, verrouiller la tête puis traiter idempotence/génération selon
   les règles existantes ; écrire opération, documents locaux, binding,
   révision/état et intention dans la même transaction que les participants
   d'audit/gouvernance déjà requis. READ ne crée pas de souhaité supplémentaire.
3. Attendre le commit propriétaire le plus externe. Une notification postcommit
   peut réveiller le relais mais ne constitue pas le mécanisme durable :
   l'outbox reste découvrable après perte de cette notification.
4. Le worker relit les lignes commitées, réserve par verrou de ligne dans une
   transaction courte et compare la révision courante. Des workers distincts
   ne possèdent pas simultanément une même réservation courante.
5. Recontrôler portée/génération, état ACTIVE, mandat/expiration, relation,
   exécutant, politique et temps ; écrire la tentative puis IO_STARTED avant
   l'appel transport. Les verrous PostgreSQL ne sont pas conservés durant l'IO.
6. PZT réalise ses contrôles d'admission/routage ; PA ses contrôles avant effet.
   Les octets, identifiants, mandat et clé natifs ne sont pas régénérés pour
   rendre une tentative différente artificiellement admissible.
7. Enregistrer le reçu ou l'incertitude sous comparaison de réservation.
   Une réservation périmée ne peut plus avancer l'état courant ; son retour
   peut être ajouté comme STALE_CALLBACK et rapproché par le résolveur.
8. Après panne ou perte de réservation avec IO_STARTED, réconcilier avant toute
   réémission. Une réservation expirée ne prouve ni arrêt de l'ancien worker,
   ni absence d'effet : la protection distante reste l'admission et
   l'idempotence/journal natifs.

Ordre de verrouillage validé : tête existante, état de liaison, intention,
puis métadonnées concernées ; ordre stable par identifiant entre plusieurs
objets. Le résolveur externe est appelé hors transaction de verrouillage,
puis son résultat est réévalué sous révisions courantes. Un timeout SQL ou
un conflit n'est pas transformé en succès.

La réservation n'ajoute aucun champ wire de fencing. Elle exclut des écritures
locales obsolètes ; elle ne garantit pas une émission réseau unique après
partition. Si les propriétaires ne peuvent établir une reprise sûre, la
demande reste suspendue/incertaine. Aucun exactement-une-fois distribué
n'est promis.

### 4.3 États locaux de l'intention

| État validé | Suites possibles | Garde |
| --- | --- | --- |
| PENDING | RESERVED, PAUSED, CANCELLED. | Commit établi ; CANCELLED exige absence d'émission. |
| RESERVED | PENDING, PAUSED, RECONCILE_REQUIRED, RECEIPT_RECORDED. | Retour PENDING seulement si absence d'IO prouvée et nouvelle tentative autorisée ; dès émission possible et issue inconnue, réconciliation obligatoire. |
| RECONCILE_REQUIRED | RECONCILE_REQUIRED, PAUSED, RECEIPT_RECORDED, CLOSED, PENDING. | PENDING seulement après preuve propriétaire d'absence d'effet/émission incompatible et droit courant de remise ; jamais sur seule expiration de réservation. |
| PAUSED | PAUSED, PENDING, RECONCILE_REQUIRED, CANCELLED. | Cause levée, contexte courant vérifié ; inconnue maintenue ou réconciliée ; annulation sans émission prouvée seulement. |
| RECEIPT_RECORDED | RECEIPT_RECORDED, RECONCILE_REQUIRED, CLOSED. | ACK vérifié arrête les remises automatiques, sans SUCCEEDED ou confirmation déduits ; lecture du résultat avec son mandat propre. |
| CLOSED | CLOSED. | Dossier de remise rapproché et résultat propriétaire connu ; la fermeture locale ne crée pas un fait Agent. |
| CANCELLED | CANCELLED. | Absence d'émission établie ; historique conservé, aucune réactivation automatique. |

Les états de binding et d'outbox sont distincts. PREPARED n'est pas RESERVED,
ACTIVE ne prouve pas une livraison, RETIRED n'efface pas une issue distante.
La suspension et le retrait suivent les transitions D-A1 ; le résultat tardif
reste attaché à sa liaison d'origine.

Les échéances de réservation, attente, concurrence et nombre de tentatives
viennent d'un profil serveur explicitement choisi et versionné. Leur absence
bloque le démarrage du relais concerné ; aucune durée ou valeur par défaut
n'est déduite de la présente décision.

### 4.4 Retours et erreurs

TransportObservation 1.0.0, privé, définit les champs exacts :
attempt_ref, outcome, receipt_ref, native_operation_ref, detail_ref.
outcome vaut RECEIPT, REFUSED_NO_SUBMISSION ou UNKNOWN. receipt_ref est requis
pour RECEIPT ; native_operation_ref est présent seulement si le propriétaire
l'a établi ; detail_ref reste une référence minimisée, sans corps secret.

REFUSED_NO_SUBMISSION exige une preuve contractuelle que cet appel n'a pas
été soumis, sans prétendre qu'une tentative antérieure n'a pas eu d'effet.
Timeout, rupture après début d'IO, parsing ambigu ou retour non vérifiable
sont UNKNOWN. Une référence de reçu non vérifiée ne classe pas RECEIPT.

Motifs privés validés : COMMIT_UNRESOLVED, BINDING_STALE, GENERATION_STALE,
CLAIM_STALE, PROVIDER_UNAVAILABLE, AUTHORITY_REFUSED, TIME_IN_DOUBT,
SUBMISSION_UNKNOWN, RECEIPT_UNVERIFIABLE, RESULT_DIVERGENT,
IDEMPOTENCE_CONFLICT et PROFILE_UNAVAILABLE. Ils restent des décisions
de diagnostic, sans ajout aux codes wire, aux phases PA ou aux issues Agent.

## 5. D-F1 — Interfaces concrètes validées

### 5.1 Composition authentique et frontière des données

Chaque interface nouvelle ci-dessous est privée, validée en version 1.0.0.
Les noms désignent des réalisations futures, pas des classes présentes.
Leur enregistrement lie slot, interface_version, provider_component,
implementation_ref, implementation_version, composition_ref et
qualification_ref. L'existence d'une référence de qualification ne prouve
pas qu'elle est valable : ses sources, version, portée et état courant sont
vérifiés par la composition compétente, sans auto-déclaration du fournisseur.

La composition sélectionne les dépendances requises ; elle ne délègue pas
l'autorisation des effets au Kernel. Les références de clé ou de preuve
restent chez leurs propriétaires ; aucun secret ou handle natif n'est
sérialisé dans les enregistrements validés.

### 5.2 Fournisseurs de stockage, autorité et transport

| Interface validée et propriétaire | Opérations et entrées détaillées | Sorties et responsabilités |
| --- | --- | --- |
| AgentBindingRepository — Agent | stage_binding(transaction propriétaire, instruction/contexte, références natives résolues) ; read_binding(scope/cible, binding_ref, autorité de lecture courante) ; transition_binding(binding_ref, expected_revision, nouvel état, motif et références de contrôles). | BindingSnapshot fermé D-A1 et révision ; stage rejoint la transaction ; transition écrit historique+état ensemble. Aucun commit implicite ni permission renvoyée. |
| AgentRelayStore — Agent | stage_submission, observe_commit, reserve_next, append_event, compare_and_transition et read_reconciliation, avec les données du §4. | Intention/réservation/événement et révisions ; accès PostgreSQL seul, aucun réseau. Chaque mutation vérifie scope, binding et jeton local attendu. |
| AgentOwnerAuthorityProvider — composition PBO via Core/Auth publics | require_management_use(instruction, contexte serveur, binding, purpose courant) ; resolve_target_binding(cible Agent, profil et références PA/PZT attendues). | Refus typé ou vérification courante effectuée ; correspondances résolues, non autoritaires par leur présence seule. Vérifie sujet, scope, droit, mandat, expiration et cible. Aucun mandat critique PA consommé par Agent. |
| InitialPaAuthorityProvider — PA/C08/Z12 | require_initial_use(invocation native, contexte initial propriétaire, purpose, plan/confirmation et références courantes). | Contrôles initiaux chez les propriétaires et refus fermés ; aucun Subject, tenant, génération Agent ou droit Core fictif avant PostgreSQL. Cette interface n'est pas fournie par AgentOwnerAuthorityProvider. |
| AgentPztTransport — PZT | submit(attempt_ref, binding_ref, référence de demande native exacte, relation/terminal attendus, contexte propriétaire courant) ; inspect_submission(référence d'invocation, cible, mandat de lecture courant). | TransportObservation pour submit ; observation propriétaire de remise pour inspect. Admission, canal et routage PZT ; aucun accès direct PBO–PA et aucune confirmation d'effet PA. E3 local reprend Cython/OpenSSL 3 mTLS. |

Les contrôles de gestion Agent utilisent les signatures publiques Core/Auth
actuelles par leurs adaptateurs. Les signatures internes validées
require_management_use/require_initial_use ne deviennent ni une nouvelle
façade universelle ni une permission stockable ; les gardes finales sont
refaites par PZT/PA avant leur effet. Une vérification préalable Agent ne
préconsomme pas un mandat PA one-shot.

### 5.3 Résultat, origine et confirmation

| Interface/adaptateur et propriétaire | Entrées exactes de l'opération validée ou existante | Sortie et refus requis |
| --- | --- | --- |
| AgentNativeResultResolver — adaptateur Agent vers le fournisseur PA | resolve_result(binding_ref, native_operation_ref, contexte de lecture actuel, expected_snapshot_ref optionnel). Le fournisseur PA relit résultat durable, journal/ancre et postconditions réelles, par PZT. | Reçu D-A1 exact à neuf champs : binding_ref, native_operation_ref, native_result_ref, native_snapshot_ref, native_revision_ref, response_digest, origin_proof_ref, postcondition_refs, time_evidence_ref ; ou refus/doute. Aucune phase ou date seule ne fournit l'ordre causal. |
| AgentOriginTrustAdapter — Agent, réalise AgentOriginTrustPort existant | verify_origin : result, context, observed_document, observed_at, source_ref, target_id, scope. Les références natives complémentaires sont résolues côté serveur depuis la liaison, sans nouvel argument client arbitraire. | tuple de Diagnostic selon le port existant ; vide seulement si contrôle réel effectué et satisfait. Vérifie origine, octets/document, cible, scope, génération, opération et snapshot propriétaire. Booléen ou chaîne de preuve seuls refusés. |
| AgentConfirmationTrustAdapter — Agent, réalise AgentConfirmationTrustPort existant | verify_confirmation : state, result, observed_fact_id, observed_source_ref, observed_origin_proof, postcondition_ref, context, target_id, scope. | tuple de Diagnostic ; vérifie le fait OBSERVED persisté et le contexte, la postcondition réelle et la confirmation autorisée distincte. Pas de passage automatique depuis SUCCEEDED et pas de confirmation d'un fait d'une autre génération. |

Les implémentations devront préserver les exceptions attendues du dépôt
AgentTrustError et les diagnostics existants, sans convertir les défauts
inattendus en réussite. unknown conserve origin_proof=None dans le résultat
Agent ; les preuves natives restent séparées et traçables.

Un reçu de résolution décrit des références ; il n'est pas une autorisation
réinjectable. L'ordre causal est établi par le propriétaire du résultat et
son snapshot courant. L'égalité lexicale de native_revision_ref ou l'ordre
des timestamps/UUID ne sert pas d'algorithme de causalité.

### 5.4 Temps : interface existante conservée

| Méthode TimeProducer 2.0.0 existante | Entrée | Sortie/sémantique préservées |
| --- | --- | --- |
| time_diagnostic | use_ref : TimePublicRef. | TimeDiagnostic à quatre champs, observation sans admission. |
| time_require_use | use_ref : TimePublicRef. | None après garde courante ; sinon TimeRefusedError ou TimeDoubtError ; None n'est pas une capacité. |
| time_ceremony_diagnostic | ceremony_ref : TimePublicRef. | Diagnostic de cérémonie sans admission. |
| time_ceremony_require_use | ceremony_ref : TimePublicRef. | Garde courante de cérémonie, mêmes principes de refus/doute. |

PBO, PA et PZT composent leurs producteurs propres avec les sources du profil
adopté. Aucun champ UTC, incertitude, pointeur ou bail n'est ajouté à
TimeDiagnostic. Les instants des messages viennent de leurs producteurs
contractuels ; TimeProducer n'est pas transformé en API now().
Les horodatages locaux de suivi ne constituent pas une source temporelle
de sécurité supplémentaire. La façade envisagée core/time_evidence.py
reste absente au contrôle ; aucun fournisseur livré n'est désigné par ce nom.

## 6. D-SMIG — Migration physique et retour validés

Aucun numéro de migration n'est réservé : il sera choisi depuis le graphe
Django courant lors d'une réalisation autorisée. Les migrations de structure,
le classement de données et l'activation du relais sont trois opérations
distinctes ; appliquer un schéma ne démarre aucun relais et n'émet rien.

| Étape déjà adoptée | Détail physique validé | Preuve et condition de passage |
| --- | --- | --- |
| M0 — Inventaire | Inventorier tables et volumes Agent, versions/écrivains/consommateurs, octets engagés et états incertains ; établir le profil de déploiement et le plan sauvegarde/restauration isolé. | Manifestes et empreintes, accès et gouvernance, compatibilité du graphe de migration, ressources/budgets retenus ; aucune donnée modifiée. |
| M1 — Extension | Créer les huit tables et index/FK/contraintes ; déployer lecteurs explicites v1/v2 avec sélection désactivée pour écritures v2 et relais ; vérifier les contraintes existantes inchangées. | Migration vide et sur copie représentative ; anciens lecteurs restent utilisables ; suppression destructive des nouvelles tables exclue du retour après données. |
| M2 — Classification | Ajouter les lignes de provenance depuis preuves de producteur et codec ; copie exacte de documents Agent admissibles seulement, sans normalisation. Ne pas fabriquer des bindings ou intentions pour les opérations historiques. | Comptages et empreintes avant/après identiques pour les anciennes lignes ; ambiguës/invalides isolées ; classement rejouable et collision de provenance détectée. |
| M3 — Coexistence | Sélection authentique des versions et des fournisseurs par consommateur ; écritures de binding/intention seulement pour les nouvelles demandes acceptées du périmètre prêt. Anciennes opérations restent en lecture/réconciliation propriétaire. | Matrice v1/v2 et composition ; identités et digests inchangés ; les validateurs 1.0.0 ne sont pas assouplis globalement pour admettre 2.0.0. |
| M4 — Activation ciblée | Après qualification du parcours complet, activer les écritures 2.0.0 sélectionnées avec provenance dans la même transaction que chaque nouvelle opération/fait ; activer séparément le relais sur ce périmètre. | Commit, concurrence, transport, autorités, résultat, postconditions et refus prouvés ; historique non réémis. Aucun consommateur v1 incompatible ne lit silencieusement un payload v2. |
| M5 — Fin des nouvelles admissions v1 | Retirer les nouvelles écritures v1 seulement après revue ; garder lecteurs et provenance historiques ; opérations en doute réconciliées ou maintenues dans un parcours isolé supporté. | Revue d'admission, compatibilité et absence de perte de données ; aucune durée ou date arbitraire de coexistence. |

Le classement est idempotent par cible/révision/contenu de provenance :
reprise identique retrouve la ligne ; divergence exige examen, sans écraser
l'historique. La liste des ambiguïtés est un résultat bloquant pour l'usage
concerné, pas une conversion supposée réussie. Les nouvelles dates six
décimales ne sont pas inventées pour les anciens faits.

Pour AgentOperation, schema_version existant est conservé et contrôlé ;
pour AgentFact la provenance de version devient explicite avant toute
interprétation v2. Les futurs lecteurs/validateurs sont sélectionnés par ce
discriminant et la composition, pas par la présence d'une fraction.
Une écriture de fait v2 et sa provenance sont atomiques, sans modifier
l'historique ou le compteur BaseAgent.version.

Retour avant écritures nouvelles : retirer la sélection, garder l'extension
inerte et les anciennes données. Après écritures v2 : conserver les lecteurs
compatibles ou bloquer le périmètre ; aucune troncature temporelle,
downmigration destructrice, remise à zéro de génération ou réactivation de
mandat. Le relais cesse d'accepter de nouvelles réservations selon son
lifecycle ; une réservation en cours ou un IO_STARTED reste à réconcilier,
sans supposer son annulation distante.

Une restauration rapproche les journaux PA/PZT, effets réels, révocations
et admissions courantes avant toute reprise. Une ancienne sauvegarde
PostgreSQL seule ne prouve pas qu'une intention n'a jamais été émise.
Les tentatives redevenues PENDING dans une copie restaurée restent bloquées
jusqu'à ce rapprochement ; aucun replay automatique du passé.

## 7. Preuves attendues et statut

Tous les repères P-SRF01–P-SRF18 sont **PRÉVUS — NON EXÉCUTÉS**.
Ils détaillent SRF01–SRF08 et les cas D/C/R existants, sans les remplacer.

| Repère | Vérification future et preuve exigée | Traçabilité |
| --- | --- | --- |
| P-SRF01 | Inventaire réel des huit tables, colonnes, FK, contraintes et index ; échec des formes interdites. | SRF01 ; C05/C21. |
| P-SRF02 | Scope/cible/acteur et génération divergents, collision de digest et comparaison intégrale ; aucun accès interscope ou deuxième binding. | SRF01 ; D02/D04. |
| P-SRF03 | Concurrence de révision, tentative d'altérer payload/historique et cycle RETIRED final ; refus démontrés par les chemins réellement utilisés. | SRF01 ; D02/D04. |
| P-SRF04 | Octets Agent signés/hachés et traces exactes ; projection JSONB incapable de remplacer les originaux ; refus de secret ou de preuve native copiée hors propriétaire. | SRF02 ; D13. |
| P-SRF05 | Transaction englobante, savepoint, rollback, commit perdu et notification postcommit perdue ; aucune émission avant commit établi. | SRF03 ; D01/D05. |
| P-SRF06 | Deux workers, réservation périmée, ancien callback et saturation des compteurs ; aucun avancement local obsolète. | SRF04 ; C20/C21. |
| P-SRF07 | Crash avant/après IO_STARTED et émission ; ancien worker retardé ; pas de réémission sur seule expiration de réservation. | SRF04/SRF05 ; D05. |
| P-SRF08 | Timeout, ACK non vérifié, reçu vérifié sans résultat, refus non émis et tentative antérieure incertaine ; pas de succès ou absence d'effet fabriqués. | SRF05 ; D06/D08/D09. |
| P-SRF09 | Rejeu natif réellement présenté au propriétaire après panne ; mandat consommé, idempotence/journal et postconditions empêchent le double effet. | SRF05 ; C20/C21. |
| P-SRF10 | Mandat révoqué/expiré, génération/relation/exécutant changé entre vérifications ; refus avant effet selon chaque propriétaire. | SRF04/SRF06 ; C09–C13/C23/C24. |
| P-SRF11 | Composition substituée, fournisseur absent ou version incompatible, faux raccord C09 Core ; refus sans repli. | SRF06 ; D16/C28. |
| P-SRF12 | Parcours initial sans Core et gestion ordinaire avec Core/Auth réels ; aucune identité ou génération synthétique. | SRF06 ; D03/C06. |
| P-SRF13 | Snapshot, ordre causal, réponse altérée, origine/postcondition manquante et résultat tardif ; reçu neuf champs et confirmation vérifiés. | SRF07 ; D07/D10/D11. |
| P-SRF14 | Producteurs PBO/PA/PZT et dégradation au point d'usage ; TimeDiagnostic/None réinjectés refusés, aucun repli now(). | SRF08 ; D12/C11. |
| P-SRF15 | Migration additive sur copie, classification rejouée, provenance absente/contradictoire ; anciennes lignes, octets, digests et UUID inchangés. | SRF02 ; D13/C22. |
| P-SRF16 | V1/v2 mixtes et même idempotence avec dates différemment encodées ; conflit explicite, pas de nouvelle opération ou conversion automatique. | SRF02 ; D14/C27. |
| P-SRF17 | Retour après écritures v2, restauration d'une intention anciennement émise et autorité révoquée ; lecteurs conservés et reprise bloquée jusqu'à rapprochement. | SRF02/SRF05 ; D15/C24. |
| P-SRF18 | Parcours intégré de gestion, effets, résultat durable, confirmation, distribution et nettoyage ; aucune qualification déduite d'une fixture. | A5 ; C28/R01–R68. |

Chaque preuve devra identifier sources et empreintes, versions des contrats
et fournisseurs, profil/plateforme, données et ressources de test autorisées,
commande effectivement exécutée, résultat observé, état durable,
postconditions, nettoyage et limites. Une validation de schéma ou un test
avec double ne remplace pas le fournisseur réel dont la garantie est visée.

Pour la qualification native future, la dernière stable Cython admissible
est sélectionnée au début de campagne puis verrouillée avec ses preuves de
sélection. Aucune version n'est téléchargée, installée ou requalifiée ici.

## 8. Références techniques et portée de validation

Le type JSONB ne conserve pas les blancs ni l'ordre ou les doublons des clés ;
les octets engagés restent donc séparés. Référence primaire :
[PostgreSQL 16 — types JSON](https://www.postgresql.org/docs/16/datatype-json.html).

Les contraintes interlignes/intertables ne sont pas confiées à un CHECK
de ligne ; FK et unicités assurent leurs garanties structurelles, complétées
par le dépôt pour les invariants métier. Référence :
[PostgreSQL 16 — contraintes](https://www.postgresql.org/docs/16/ddl-constraints.html).

Les verrous de ligne structurent les transactions locales, sans prouver
une exclusion ou un effet distant. Référence :
[PostgreSQL 16 — verrouillage](https://www.postgresql.org/docs/16/explicit-locking.html).

Les contrôles documentaires portent sur ces décisions et leurs renvois.
Ils vérifient la cohérence de leur inscription sans qualifier un fournisseur,
une migration ou un exécutable. La validation du développeur ne remplace pas
les réalisations et preuves produit encore manquantes.

## 9. Vérifications historiques de la proposition avant adoption — 27 octobre 2026

| Contrôle réellement exécuté | Résultat |
| --- | --- |
| Documents et renvois | Douze documents contrôlés, UTF-8/LF, absence d'espaces de fin de ligne, 130 liens relatifs existants. |
| Structure de la proposition | Huit tables privées, dix-huit repères de preuve ordonnés et uniques, statut NON VALIDÉES explicite, aucune production de code dans le document. |
| Conservation du périmètre | Deux canons, deux deltas, tâches/cases et documents de décision antérieurs contrôlés inchangés ; 83 fichiers de sources/configuration inchangés par empreinte. |
| OpenSpec strict ciblé | PA01, PA10, pixs-agent et pzt valides. |
| OpenSpec global standard et strict | 185/185 dans chaque mode : 107 évolutions et 78 spécifications ; zéro avertissement et zéro erreur, mêmes 86 informations qu'au relevé préalable. |
| Espaces Git | Contrôle réussi sur les quatre documents concernés. |

Un document de détail est créé et trois renvois de cadrage sont actualisés.
Les invariants D-A1/D-A2/D-A3/D-MIG et S1/R1/F1 sont conservés ; les
choix supplémentaires D-S1/D-R1/D-F1/D-SMIG restent proposés à validation.
Ces contrôles ne sont ni une validation du développeur, ni une migration,
ni une compilation, ni une recette fonctionnelle. Les réalisations et
preuves produit restent manquantes.

## 10. Adoption documentaire et état résultant — 27 octobre 2026

La validation explicite du développeur couvre D-S1, D-R1, D-F1 et D-SMIG
tels que détaillés ci-dessus. Elle ne vaut ni réalisation ni preuve produit.

| Dimension | État après inscription |
| --- | --- |
| D-S1 | VALIDÉ : huit tables, colonnes/types/nullabilités, clés/contraintes/index, séparation état/payload et codecs privés. |
| D-R1 | VALIDÉ : contrat AgentRelay 1.0.0, commit propriétaire, réservation, tentatives, sept états locaux, retours et réconciliation. |
| D-F1 | VALIDÉ : interfaces privées, composition, résolution/origine/confirmation et TimeProducer 2.0.0 conservé. |
| D-SMIG | VALIDÉ : migration physique additive M0–M5, classification, coexistence, activation séparée et retour/restauration. |
| Deltas normatifs | INSCRITS dans PA01 : seize exigences/trente-deux scénarios pixs-agent et une exigence/deux scénarios pzt. |
| Canon pour ces nouveaux détails | NON SYNCHRONISÉ par cette inscription ; canons et décisions antérieures conservés. |
| Réalisations encore manquantes | Modèles/dépôts/DDL/migrations, codecs/validateurs et consommateurs v2, relais/hébergement/profils, fournisseurs exécutables/versionnés et raccordements réels. |
| Preuves encore manquantes | P-SRF01–P-SRF18, C01–C28, D01–D16 et recettes intégrées applicables : aucune nouvelle exécution ici. |
| Statut produit | Agent 2.0.0 NON LIVRÉ, migration NON EXÉCUTÉE ; qualification fonctionnelle PA/PZT BLOQUÉE. |

Aucune tâche n'est cochée ; aucune source, configuration de déploiement,
donnée, autorité ou service n'est modifié par cette inscription.

## 11. Vérifications de l'inscription validée — 27 octobre 2026

| Contrôle réellement exécuté | Résultat observé |
| --- | --- |
| Documents et renvois | Seize documents contrôlés : UTF-8/LF, fins de fichier, espaces de fin de ligne et 192 liens relatifs existants. |
| Ajouts normatifs | Dix-sept exigences et trente-quatre scénarios ; titres uniques, préfixes des deux deltas antérieurs conservés octet pour octet. |
| Correspondance du détail | Seize contrats détaillés Agent identiques aux sections validées ; ligne de l'interface PZT et observations privées identiques au détail. Les sections techniques restent identiques à la proposition adoptée, après changement des seuls termes de statut. |
| Schéma et preuves | Huit tables et dix-huit repères P-SRF01–P-SRF18 contrôlés ; tous les repères restent NON EXÉCUTÉS. |
| OpenSpec strict ciblé | PA01, PA10, pixs-agent et pzt valides. |
| OpenSpec global standard et strict | 185/185 dans chaque mode : 107 évolutions et 78 spécifications ; zéro avertissement et zéro erreur, mêmes 86 informations qu'au relevé préalable. |
| Canons et tâches | Deux canons inchangés par empreinte ; aucune synchronisation des nouveaux détails ; listes de cases PA01/PA10 inchangées. |
| Espaces Git | Contrôle réussi sur les quatorze documents concernés. |

Le relevé de 90 fichiers de sources/configuration constate 88 empreintes
inchangées et des évolutions de generator.py et builder.py dans
src/pixs/pa_native pendant l'intervention, hors des écritures documentaires
de ce travail. Ces sources sont conservées sans intervention et ne sont ni
testées ni qualifiées par cette inscription. Les contrôles de conservation
documentaire, des canons et des cases ne leur attribuent aucune preuve.

Aucun code, DDL ou migration n'est produit ; aucune compilation, recette
produit, migration ou activation n'est exécutée par ce travail documentaire.
