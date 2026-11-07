# PA/PZT — Décisions détaillées A1, A2 et A3 avec migration

Date : 26 octobre 2026.

Complément validé le 27 octobre 2026 : [S1/R1/F1](DECISIONS_S1_R1_F1.md)
fixe les tables PostgreSQL privées dédiées Agent, l'outbox/relais PBO vers
PZT et les fournisseurs par domaine. Les mentions ci-dessous de choix
physiques ou de remise encore à arrêter décrivent le périmètre D du
26 octobre ; elles sont complétées par ces décisions acquises.
Les modèles et tables D-A1/D-A2/D-A3/D-MIG restent inchangés.
Les cinq exigences et douze scénarios S1/R1/F1 sont synchronisés à l'identique
aux canons pixs-agent/pzt sur demande explicite complémentaire du développeur
le 27 octobre 2026. Cette synchronisation ne réalise aucun de ces raccords.

Le développeur valide ensuite [D-S1/D-R1/D-F1/D-SMIG](DETAIL_S1_R1_F1.md)
le 27 octobre 2026 : les schémas et interfaces détaillés sont désormais
adoptés dans les deltas PA01, sans synchronisation de ces nouveaux détails
au canon. Les mentions de schéma à détailler ci-dessous conservent le
périmètre antérieur ; modèles, migrations, fournisseurs et preuves restent
à réaliser. Le contenu D-A1/D-A2/D-A3/D-MIG est conservé.

## 1. Statut et autorité

**D-A1, D-A2, D-A3 ET D-MIG VALIDÉS PAR LE DÉVELOPPEUR — DOCUMENTATION UNIQUEMENT.**

Les orientations [A1–A5](DECISIONS_A1_A5.md) sont validées et synchronisées
dans les canons [pixs-agent](../../specs/pixs-agent/spec.md) et
[pzt](../../specs/pzt/spec.md). Le développeur valide explicitement D-A1,
D-A2, D-A3 et D-MIG le 26 octobre 2026 et demande leur inscription dans les
spécifications et le cadrage, sans implémentation ni production de code.
Les structures logiques privées, transitions précises, version `2.0.0`,
codec de contenu et stratégie de migration ci-dessous sont donc adoptés.
Ils sont inscrits dans le delta pixs-agent PA01 et, sur demande explicite
complémentaire du développeur le 26 octobre 2026, leurs quatorze exigences
et vingt-cinq scénarios sont synchronisés à l'identique dans le
[canon pixs-agent](../../specs/pixs-agent/spec.md), sans réapplication des
autres deltas. Cette synchronisation ne les rend pas livrés.

Les noms de champs désignent un modèle logique validé, pas des colonnes SQL
créées, des classes installées ou un nouveau format transmis à PA. Aucun
plafond, délai de coexistence, identifiant de migration ou outil supplémentaire
n'est fixé. Les règles et bornes propriétaires existantes restent applicables.

Références : [cadrage fonctionnel](CADRAGE_FONCTIONNEL.md),
[contrats PA01](contracts.md), [raccords PA10](../separate-pa-pzt-and-pbo-management-modules/RACCORDS.md),
[recette C01–C28](../separate-pa-pzt-and-pbo-management-modules/RECETTE_RACCORDS.md),
[contrats Agent actuels](../../../src/pixs/agent/contracts.py),
[stockage Agent](../../../src/pixs/agent/models.py),
[identités et digests](../../../src/pixs/agent/identifiers.py).

## 2. Contraintes observées à préserver

| Source actuelle | Conséquence pour le détail proposé |
| --- | --- |
| Agent expose les issues fermées `ack`, `confirmed`, `failed`, `unknown`. | Ne pas ajouter une phase native à cet enum par simple raccordement. |
| `unknown` impose `origin_proof=None` dans le résultat Agent. | Conserver les preuves natives chez leurs propriétaires et dans la traçabilité privée ; ne pas les recopier dans ce champ incompatible. |
| `AgentOperation.id` et `request_operation_id` sont distincts. | Ne pas prendre la clé de stockage pour l'identifiant logique d'une requête. |
| Une nouvelle opération souhaitée stockée possède une génération issue de la persistance Agent. | Le raccord ne crée pas lui-même un compteur ni un incrément supplémentaire. Une lecture ne devient pas une mutation du souhaité. |
| `agent-content.v1` engage notamment `schema_version` et `expires_at`. | Réécrire une date ancienne ou sa version invaliderait le contenu canonique et son digest ; l'historique reste intact. |
| La validation et les champs temporels Agent 1.0.0 exigent UTC à la seconde. | Une précision native à six décimales demande une version et des consommateurs explicitement sélectionnés. |
| E4/E5 conservent leurs octets, digests et versions propres. | Aucun réencodage de preuve native et aucun changement implicite de leurs messages. |

## 3. A1 — Liaison serveur validée D-A1

### 3.1 Propriété et périmètre

Le modèle retenu est un enregistrement privé `AgentPaBinding`, schéma `1.0.0`, possédé
par Agent dans sa persistance serveur. Il lie un contexte de gestion ordinaire
accepté aux références PA/C08/PZT résolues par leurs propriétaires.
Ce nom ne crée ni contrat public ni capacité ; la forme physique du stockage
reste à arrêter avant une éventuelle migration de données.

La liaison n'est ni un mandat ni une preuve d'autorité durable. Son existence,
son état ACTIVE et son empreinte ne dispensent jamais des gardes courantes
A4 avant effet. Le contexte initial C08/PA avant PostgreSQL reste séparé et
ne reçoit pas de génération Agent artificielle.

### 3.2 Modèle logique fermé validé

Racine : exactement `schema_version`, `binding_ref`, `revision`, `state`,
`agent`, `native`, `audit`. Les objets imbriqués ont les champs ci-dessous.
Une référence est opaque et non autoritaire ; sa forme ne remplace pas sa
résolution. Les textes, collections et entiers ont les bornes du profil
protégé explicitement sélectionné, sans valeur par défaut ajoutée ici.

| Racine | Type et règle validés |
| --- | --- |
| `schema_version` | Version exacte `1.0.0` de cette liaison privée, distincte des versions Agent et PA. |
| `binding_ref` | Référence serveur stable, non choisie par le client ; indépendante des identifiants d'opération et des digests. |
| `revision` | Entier exact positif, booléens refusés ; révision locale de concurrence, jamais génération Agent ou compteur PA. |
| `state` | PREPARED, ACTIVE, SUSPENDED ou RETIRED, selon le cycle validé ci-dessous. |
| `agent`, `native`, `audit` | Objets fermés définis ci-dessous ; aucune donnée secrète. |

| Objet `agent` : champs exacts | Origine et couplage validés |
| --- | --- |
| `request_kind` | MUTATION ou READ, déterminé par l'opération/profil serveur, jamais par une déclaration cliente seule. |
| `contract_version` | Version du contrat Agent réellement sélectionné et validé, sans déduction depuis la longueur d'une date. |
| `operation_ref` | Référence de l'AgentOperation persistée pour MUTATION ; absence explicite pour READ si aucune opération souhaitée n'est créée. |
| `request_operation_id` | Identifiant logique de l'invocation de gestion, distinct de `operation_ref`. |
| `scope_context` | ScopeContext existant, validé dans sa forme et son autorité courantes. |
| `actor_ref` | Acteur initial issu de la source serveur compétente ; aucune identité fabriquée depuis un opérateur natif ou un UID. |
| `pa_target` | Cible Agent, rapprochée des références natives par le fournisseur propriétaire. |
| `expected_generation` | Génération attendue de l'instruction/contexte accepté. |
| `bound_generation` | Génération réellement attribuée à l'opération persistée, ou génération serveur validée pour READ ; aucun calcul depuis époque/séquence/NV. |
| `request_digest` | SHA-256 du contenu canonique Agent accepté (`content_digest`), sous le codec lié à sa version ; pas un digest de tous les champs du message ni un substitut du digest natif. |
| `idempotency_key` | Clé acceptée dans le domaine existant acteur/scope/cible/opération/version ; pas de nouveau domaine permis par un changement de contrat temporel. |

| Objet `native` : champs exacts | Origine et couplage validés |
| --- | --- |
| `protocol_profile` | Profil propriétaire explicitement sélectionné : messages 1.0.0 ou enveloppes E5 1.1.0 ; les deux restent distincts. |
| `catalog_operation`, `catalog_version` | Opération et version du catalogue fermé livré, vérifiées côté serveur. |
| `purpose` | Purpose E5 exact quand le profil l'exige ; absence explicite dans le profil 1.0.0 sans purpose, sans le fabriquer. |
| `request_operation_id` | Identifiant de l'invocation native ; aucune égalité supposée avec les identifiants Agent. |
| `subject_operation_ref` | Opération technique lue pour READ_RESULT ; absence hors cette branche. Résolution et autorisation de lecture actuelles obligatoires. |
| `installation_ref`, `target_ref` | Références natives rapprochées de la cible Agent par des sources compétentes. |
| `pzt_relation_ref`, `executor_terminal_ref` | Relation et exécutant attendus résolus et vérifiés ; une reconnexion ne change pas silencieusement leur identité. |
| `request_digest` | Digest prescrit par le profil natif ; pour E5, il engage l'enveloppe entière, pas seulement NativeRequest. |
| `trace_binding_ref` | Référence à la liaison vérifiée des corrélations/causalités ; ordre et doublons signés conservés, sans réduction à une seule corrélation. |

| Objet `audit` : champs exacts | Origine et couplage validés |
| --- | --- |
| `accepted_at` | Instant d'acceptation serveur exact en UTC à six décimales ; ne vaut pas autorité temporelle à lui seul. |
| `authority_context_ref` | Référence au contexte vérifié et à ses sources propriétaires ; aucun credential ni permission consommée réutilisable. |
| `time_evidence_ref` | Référence de traçabilité à la preuve temporelle ; usage courant encore recontrôlé auprès du producteur. |
| `state_reason_ref` | Absence explicite lorsque non requise ; raison propriétaire inspectable pour suspension ou retrait, sans restitution de secret. |

Les couples de références n'impliquent pas une correspondance calculable.
Une cible ou relation ambiguë bloque la création utilisable de la liaison.
Les octets de la requête native et de ses preuves restent chez leurs
propriétaires ; un digest seul n'en démontre ni origine ni validité.

### 3.3 Création, atomicité et idempotence

MUTATION désigne ici un changement du souhaité Agent et READ une lecture
sans ce changement. Ces catégories ne sont pas les classes de sensibilité
ou d'effet du catalogue natif ; leur sélection dépend du parcours Agent
réellement accepté, pas du seul nom de l'opération PostgreSQL.

Pour MUTATION, le mécanisme retenu prévoit la persistance de l'opération Agent, de la liaison
et de l'intention d'envoi dans une même transaction propriétaire, sous les
contrôles actuels de scope, génération et idempotence. Le résultat de commit
est rapproché avant de remettre la demande à PZT. Le contenu canonique exact
et la génération viennent de la persistance Agent, pas du raccord.

Une transaction locale n'est pas une transaction distribuée avec PA. L'envoi
réseau commence après le commit local vérifié. Si le commit ou l'envoi est
incertain, conserver l'incertitude et réconcilier les propriétaires avant
nouvelle émission ; ni l'intention persistée ni une réponse perdue ne prouve
la livraison ou l'absence d'effet. Le mécanisme physique d'intention d'envoi
reste à choisir dans les dispositifs du projet, sans nouvelle dépendance ici.

Pour READ, enregistrer le contexte accepté sans incrément de génération
du souhaité. READ_RESULT porte sa propre invocation et son propre mandat
de lecture, séparés de l'opération lue et d'un mandat critique consommé.
Une lecture d'une opération initiale C08/PA conserve ce contexte initial ;
elle ne lui attribue pas rétroactivement une opération ou génération Agent.

Un rejeu identique retrouve la liaison et le résultat connus sans nouvel
effet ni nouvelle génération. La même identité d'idempotence avec contenu,
cible, contexte ou version divergents est refusée. Aucun suffixe de version
temporelle ne transforme un rejeu conflictuel en nouvelle opération.

### 3.4 Cycle de liaison et concurrence validés

| État | Passage admis validé | Condition et limite |
| --- | --- | --- |
| PREPARED | ACTIVE, SUSPENDED ou RETIRED. | Contexte complet, commit et gardes vérifiés avant ACTIVE ; absence d'émission prouvée avant retrait sans effet. |
| ACTIVE | SUSPENDED ou RETIRED ; maintien sous recontrôles courants. | Une perte de source, divergence ou issue incertaine suspend ; un changement incompatible de cible/génération retire l'usage courant. |
| SUSPENDED | ACTIVE uniquement après réconciliation et gardes actuelles satisfaites, ou RETIRED. | Aucun nouvel effet si une issue reste inconnue ; aucune réutilisation d'un mandat consommé. Si une nouvelle invocation est nécessaire, elle a son contexte et sa liaison propres. |
| RETIRED | Aucun retour vers ACTIVE. | Conservation historique selon gouvernance et droits de lecture courants, sans capacité d'effet restaurée. |

Le payload de rapprochement Agent/natif est immuable après création ; seules
révision, état et traçabilité du changement évoluent sous contrôle de
concurrence. Une nouvelle cible, identité, génération ou requête crée une
nouvelle liaison après autorisation, pas une réaffectation de l'ancienne.
Les références d'autorité et de temps de l'acceptation restent historiques ;
les vérifications au point d'usage sont tracées séparément, sans remplacer
l'instant d'acceptation ni faire passer sa preuve pour une autorité courante.
Les gardes du transport et de l'exécutant restent nécessaires : la révision
de cette ligne ne constitue pas à elle seule un fencing sur PA.

Un résultat tardif reste lié à sa génération et son opération d'origine.
Il ne remplace pas l'état courant d'une génération suivante. L'inspection
historique exige une autorité de lecture actuelle et ne réactive pas la
liaison retirée. Les durées de conservation et d'expiration restent celles
des politiques propriétaires, sans TTL inventé.

### 3.5 Reçu interne de résolution validé

Pour appliquer A2, le reçu retenu est une preuve privée résolue par le fournisseur
compétent, liant exactement : `binding_ref`, `native_operation_ref`,
`native_result_ref`, `native_snapshot_ref`, `native_revision_ref`,
`response_digest`, `origin_proof_ref`, `postcondition_refs`,
`time_evidence_ref`. Ces références ne sont ni de nouveaux champs NativeResult,
ni des permissions, ni une preuve par simple présence.

Le fournisseur établit le snapshot, sa version courante et son ordre causal.
Une date ou un numéro fourni par le client ne décide pas quel résultat est
plus récent ; un compteur natif n'est pas converti en génération Agent.
Sans source permettant cette résolution, le rapprochement reste bloqué.
Le contrat concret de ce fournisseur reste dépendant d'A4.

## 4. A2 — Transitions et projection validées D-A2

### 4.1 Machine de phase côté producteur natif

Cette table fixe les transitions internes validées d'une invocation. Le consommateur
peut ne pas voir tous les états intermédiaires : il résout un snapshot courant
chez le propriétaire avant tout rapprochement, sans inventer les événements
manquants. Un message non authentifié ou non lié n'avance aucun état.

| Phase source | Suite validée | Conditions |
| --- | --- | --- |
| Nouvelle invocation | RECEIVED ou BLOCKED. | Accusé d'une demande liée, ou précondition refusée avant exécution. Une requête invalide sans contexte n'obtient pas un résultat propriétaire fabriqué. |
| RECEIVED | RUNNING, SUCCEEDED, FAILED ou BLOCKED. | SUCCEEDED direct admis pour une opération achevée avec ses preuves ; FAILED seulement pour une issue connue ; aucun RUNNING artificiel imposé à une lecture synchrone. |
| RUNNING | RUNNING, SUCCEEDED, FAILED ou IN_DOUBT. | La progression ne prouve pas un effet. Si l'issue d'un effet possible n'est pas connue, IN_DOUBT, pas FAILED ou BLOCKED pour masquer l'incertitude. |
| IN_DOUBT | IN_DOUBT, SUCCEEDED ou FAILED. | Résolution depuis résultats durables et postconditions réels ; pas de rejeu automatique de l'effet et pas de disparition de l'incertitude par péremption. |
| SUCCEEDED, FAILED ou BLOCKED | Même résultat terminal répété à l'identique. | Pas de retour à RECEIVED/RUNNING. Une nouvelle invocation autorisée est distincte ; un résultat contradictoire déclenche une divergence à réconcilier. |

La phase appartient à l'invocation identifiée. SUCCEEDED de PREPARE_PLAN
prouve le planning prévu par son contrat, pas une préparation PostgreSQL.
SUCCEEDED de READ_RESULT ne confirme pas l'effet de l'opération lue : celle-ci
est identifiée séparément par `subject_operation_ref` et résolue chez PA.

### 4.2 Projection vers les issues Agent

| Phase et conditions vérifiées | Résumé validé | État observé et confirmation |
| --- | --- | --- |
| RECEIVED, origine et liaison vérifiées. | `ack` possible pour la seule réception. | Aucune application, aucun document appliqué ni fait CONFIRMED déduit. |
| RUNNING courant. | Pas de nouvelle issue à fabriquer ; un `ack` antérieur reste un reçu historique. | Progression conservée chez PA ; aucune application ni fraîcheur d'observation renouvelée depuis ce seul progrès. |
| SUCCEEDED avec résultat durable, contexte et origine vérifiés. | Pas de `confirmed` immédiat depuis la phase. | Résoudre les observations et postconditions ; leur admission comme fait observé suit le port d'origine Agent. La confirmation est une étape séparée. |
| Fait observé admis, puis confirmation et postcondition vérifiées dans le contexte courant. | `confirmed`. | Fait CONFIRMED lié au fait OBSERVED réel, aux mêmes opération/cible/scope/génération et aux preuves requises. |
| FAILED, échec connu et preuve d'origine/contextes vérifiés. | `failed`. | Diagnostic d'échec, sans fabriquer un document appliqué ni supprimer les éventuels effets connus à réconcilier. |
| IN_DOUBT ou issue de transport/commit réellement inconnue. | `unknown` lorsque le contrat et le contexte le permettent. | `origin_proof=None` dans ce résultat Agent ; preuves natives et références de réconciliation conservées séparément, sans application ou confirmation supposée. |
| BLOCKED. | Refus typé de précondition et phase native BLOCKED ; pas d'issue `failed` d'exécution fabriquée. | Pas d'état appliqué ni de confirmation. Un reçu antérieur reste un reçu ; le refus et sa raison restent consultables sous autorité courante. |

OBSERVED est un type de fait de stockage, pas un synonyme de SUCCEEDED.
La structure actuelle permet aussi des observations d'échec ou d'incertitude ;
leur type ne prouve pas un état appliqué. Un document observé n'est admis que
si son origine, sa date et son contenu sont effectivement vérifiés.

La progression et les refus techniques restent accessibles au résolveur
interne de gestion sous autorité courante, distincts du document appliqué.
Cette décision n'ajoute pas une nouvelle phase à AgentManagementResult
et ne définit pas implicitement un nouvel endpoint public de progression.

### 4.3 Refus, doublons et réordonnancement

Avant projection, rapprocher liaison A1, identité et relation PZT, opération
de requête et éventuel sujet de lecture, profil/version, génération, contexte,
provenance et état courant. Un résultat plus ancien ou reçu hors ordre ne
fait pas régresser une observation confirmée. Sa date seule ne détermine
pas l'ordre : employer le snapshot propriétaire courant et sa preuve causale.

Une notification répétée se rapproche de sa preuve immuable ; elle ne crée
pas de deuxième effet, de deuxième génération ou de confirmation fictive.
Le mécanisme exact de déduplication des faits reste à aligner avec la
persistance Agent, sans promettre une unicité déjà livrée.

Une perte d'autorité interdit la projection protégée ou l'effet suivant.
Une ancienne confirmation peut rester une trace historique, jamais une
confirmation courante sans contrôle de fraîcheur et de contexte. Le contrat
exact des erreurs de transport/gestion reste à raccorder aux diagnostics
existants ; aucun nouveau vocabulaire public n'est adopté ici.

## 5. A3 — Contrat temporel Agent 2.0.0 validé D-A3

### 5.1 Version et frontières

Le numéro retenu est **2.0.0**, car une forme canonique à six décimales obligatoires
n'est pas interchangeable avec la grammaire 1.0.0 à la seconde. Ce numéro
est adopté documentairement, sans descripteur exécutable enregistré ni contrat livré. Les mêmes identifiants publics
`pixs.agent.management.command`, `pixs.agent.management.query` et
`pixs.agent.management.service` porteraient cette nouvelle version exacte.
Leur sélection relève de la composition authentique et de la compatibilité
des consommateurs, sans négociation implicite par la forme d'une date.

La version retenue conserve les champs, types non temporels, champs fermés et
issues des quatre objets Agent existants. L'instruction porte la version
de schéma 2.0.0 ; contexte, état et résultat sont identifiés par leurs types
et contrats versionnés sélectionnés, sans champ de version ajouté silencieusement
à leurs formes 1.0.0. Les limites et garanties propriétaires sont conservées.

| Objet | Champ temporel concerné | Règle 2.0.0 validée |
| --- | --- | --- |
| AgentValidationContext | `now_iso` | Instant UTC exact fourni par la source compétente ; aucune lecture d'horloge locale ajoutée par le validateur. |
| AgentManagementInstruction | `expires_at` | Échéance UTC exacte, contrôlée sans arrondi et recontrôlée au point d'usage. |
| AgentManagementResult | `occurred_at` | Instant exact de l'événement selon son fournisseur vérifié ; pas une date cliente utilisée comme preuve. |
| AgentManagementState | `observed_at`, `last_known_at` | Instants exacts ; absence conservée avec absence de document, observation actuelle et dernier connu toujours distincts. |

La forme textuelle retenue est `YYYY-MM-DDTHH:MM:SS.ffffffZ` : UTC explicite,
six chiffres fractionnaires, calendrier valide et règles de secondes du
contrat natif sélectionné. Rejeter les dates naïves, offsets alternatifs,
fractions de longueur différente et normalisations silencieuses. Aucun
profil supplémentaire de seconde intercalaire n'est introduit ici.

Comparer les instants avec une précision entière ou un type temporel exact,
sans passage par un nombre flottant. Les règles existantes de non-futur,
d'échéance, d'ordre observé/dernier connu et de fraîcheur restent applicables
avec la précision conservée et les bornes du profil sélectionné.

Six décimales décrivent une représentation ; elles ne prouvent ni précision
physique, ni synchronisation UTC, ni incertitude admissible. Le producteur
de temps et ses gardes restent indispensables. L'affichage à la seconde
est une vue seule ; il n'alimente ni empreinte ni décision de sécurité.

### 5.2 Codecs et empreintes validés

Conserver `agent-head.v1` et `agent-idem.v1` si leurs domaines et champs
restent inchangés ; ne pas ajouter la version temporelle au domaine
d'idempotence pour permettre un deuxième effet. Le codec retenu est `agent-content.v2`
pour le nouveau contenu, avec schéma 2.0.0 et dates exactes à six décimales.

Le contenu retenu garde exactement les clés du contenu actuel : `codec`,
`schema_version`, `operation_name`, `operation_version`, `subject_id`,
`scope_type`, `tenant_id`, `scope_id`, `target_id`, `expected_generation`,
`params_canonical`, `mandate_ref`, `expires_at`. Seuls le codec sélectionné,
la version de schéma et la grammaire de l'échéance évoluent. Les validations
de scope, de paramètres canoniques, de version de catalogue et les bornes
numériques existantes sont conservées ; booléen n'est pas entier.

L'encodage déterministe retenu reste celui de v1 : JSON UTF-8, clés triées,
séparateurs compacts, Unicode conservé sans normalisation implicite,
pas de NaN, infini, doublon ou champ supplémentaire. `params_canonical`
reste une chaîne canonique déjà validée, sans transformation en objet.
Le digest de contenu est le SHA-256 hexadécimal des octets UTF-8 ainsi
produits, sans LF ajouté. Cette définition détaillée est validée ;
aucun codec v2 n'est implémenté par le présent document.

Les anciens contenus `agent-content.v1`, octets signés, digests et clés
d'idempotence ne sont jamais réécrits ou recalculés comme s'ils étaient v2.
Les signatures/digests E4/E5 restent attachés aux octets natifs originaux ;
le codec Agent n'est pas un nouveau canon de signature PA.

## 6. Migration additive validée D-MIG

### 6.1 Données et compatibilité

Les modèles actuels contiennent des dates contractuelles sous forme de texte
et des métadonnées de stockage UTC distinctes. Le compteur entier `version`
de BaseAgent n'est pas la version sémantique du contrat et ne devient pas
2.0.0 par migration. Les références d'opération, générations, scopes,
identités et faits historiques restent stables.

Les dates de suivi de migration restent des métadonnées distinctes ; elles
ne remplacent pas les dates contractuelles ou la provenance des événements
historiques. Une table de suivi séparée permet de classifier sans réécrire
les lignes anciennes ; le choix physique reste à valider.

Le discriminant privé retenu est `payload_contract_version`, dans une extension
de stockage ou une table de métadonnées à arrêter, et une provenance de
classification. La version n'est pas devinée depuis la seule présence d'un
point décimal. AgentOperation porte déjà `schema_version`, conservé pour les
lignes anciennes ; les faits sans version explicite exigent une provenance
de producteur et une validation avant classification. Une ligne ambiguë
reste non interprétée comme v2 et bloque son usage protégé.

Une vue de lecture peut représenter une ancienne date à la seconde avec
`.000000Z`, en indiquant séparément sa précision de source et son contrat
d'origine. Cette vue ne réécrit ni la date stockée ni son digest ; elle
n'invente pas une résolution microseconde et n'alimente pas une preuve
native à la place de la source d'origine. Une date ancienne invalide ou
sans provenance n'est pas corrigée silencieusement.

### 6.2 Étapes et conditions de passage

| Étape | Opération future validée comme stratégie | Condition de passage et preuve attendue |
| --- | --- | --- |
| M0 — Inventorier | Identifier producteurs/consommateurs 1.0.0, profils, données contractuelles, digests, opérations en cours et issues inconnues. | Versions et empreintes rapprochées ; sauvegarde et restauration isolées préparées ; aucun format modifié. |
| M1 — Étendre | Préparer une migration additive des métadonnées de version/provenance et les lecteurs nécessaires, sans transformer les anciens contenus. | Retour à la lecture précédente vérifié avant activation ; clés/contraintes et autorisations conservées ; aucune migration exécutée par le présent document. |
| M2 — Classifier et lire | Classifier les anciens enregistrements depuis provenance et codec ; fournir des vues de lecture distinctes et identifier les lignes ambiguës. | Octets/digests/identités historiques inchangés ; aucune ligne promue en fait courant ou confirmé par le seul classement. |
| M3 — Coexister | Sélectionner explicitement le contrat par consommateur et opération ; conserver les lecteurs 1.0.0 et les nouveaux lecteurs 2.0.0. | Matrice de compatibilité et composition vérifiées ; pas de repli automatique en 1.0.0 après erreur de validation ou perte de précision. |
| M4 — Activer les nouvelles écritures | Émettre en 2.0.0 uniquement sur les parcours sélectionnés et qualifiés ; les opérations déjà acceptées gardent leur contenu/version d'origine. | Fournisseurs et consommateurs compatibles, gardes A4 courantes, refus et reprise testés ; une seule opération/liaison autorisée pour le même contexte d'idempotence. |
| M5 — Retirer les nouvelles écritures v1 | Fermer les admissions 1.0.0 du périmètre migré lorsque les consommateurs et opérations en cours le permettent. | Revue explicite du périmètre, opérations v1 et issues inconnues réconciliées ou maintenues dans un parcours isolé supporté ; lecteurs historiques conservés selon gouvernance. |

Aucune durée de coexistence ni date de bascule n'est choisie ici. Le retrait
des écritures 1.0.0 dépend de critères vérifiés, pas de l'âge du déploiement.
Une opération IN_DOUBT n'est pas relancée ou effacée pour achever M5.

### 6.3 Rejeux entre versions

Une opération acceptée en 1.0.0 garde ses octets, son codec et sa liaison.
Le même identifiant d'idempotence ne crée pas une nouvelle opération en
2.0.0. Si le contenu diffère, même par ajout de zéros fractionnaires, signaler
le conflit ; ne pas supposer une équivalence sémantique de contenus engagés
par des digests différents. L'appelant relit l'opération existante sous une
autorité de lecture courante ; aucun effet n'est rejoué automatiquement.

Une nouvelle intention réellement différente suit une nouvelle autorisation
et l'idempotence propriétaire ; le changement de version n'est pas à lui seul
une nouvelle intention. Les contrôles du journal PA restent distincts de
l'unicité locale de la liaison Agent.

### 6.4 Retour arrière et restauration

Avant toute écriture v2, le retour peut retirer sa sélection et conserver
les données originales intactes. Après des écritures v2, garder un lecteur
v2 compatible ou bloquer le périmètre : un ancien binaire incapable de lire
ces données ne les convertit pas automatiquement à la seconde.

Ne pas supprimer les nouvelles données, réécrire l'historique, restaurer
une ancienne génération ou réactiver un mandat révoqué pour revenir en v1.
Une restauration rapproche versions, révocations et opérations incertaines
avec les propriétaires courants avant reprise. Les migrations descendantes
destructives et transformations de signatures sont exclues de cette stratégie validée.

## 7. Plan de vérification documentaire et future recette

Tous les cas D01–D16 sont **PRÉVUS — NON EXÉCUTÉS**. Ces identifiants
organisent le présent document ; ils ne remplacent pas C01–C28 ou R01–R68
et ne créent pas de nouvelles cases de tâche.

| Cas | Vérification future et preuve attendue | Correspondance existante |
| --- | --- | --- |
| D01 | Création de liaison avec commit connu ; aucun envoi avant commit et aucune hypothèse d'atomicité distribuée. | C05/C20/C21. |
| D02 | Même clé identique, contenu divergent, concurrence de générations et de révisions : pas de deuxième effet ni réaffectation de liaison. | C05/C21. |
| D03 | READ_RESULT distingue requête de lecture et sujet, ne consomme pas un ancien mandat critique et n'incrémente pas le souhaité. | C06. |
| D04 | Cible/relation/génération changée et résultat tardif : conservation historique sans état courant attribué à une autre opération. | C05/C18/C23. |
| D05 | Crash, perte de source ou issue d'envoi inconnue : suspension/réconciliation, sans réutilisation de permission consommée. | C09/C20/C24. |
| D06 | RECEIVED/RUNNING : reçu ou progression seuls, aucun appliqué/confirmé et pas de fraîcheur artificielle. | C14. |
| D07 | SUCCEEDED, puis origine/postcondition/confirmation présentes ou absentes : seul le parcours entièrement vérifié confirme Agent. | C15/C17–C19. |
| D08 | FAILED et IN_DOUBT : distinction échec/incertitude, `unknown` sans preuve d'origine embarquée et preuves natives séparées conservées. | C16/C20. |
| D09 | BLOCKED et refus de précondition : aucun échec d'exécution ou document appliqué fabriqué. | C09/C16. |
| D10 | SUCCEEDED de planning ou de lecture n'est pas le succès de préparation du sujet. | C06/C07/C15. |
| D11 | Notifications dupliquées, anciennes ou contradictoires : résolution propriétaire courante et absence de régression/double confirmation. | C17–C23. |
| D12 | Instants à six décimales, bornes exactes, formats non canoniques et source temporelle dégradée : refus sans arrondi ni nouveau seuil. | C04/C11. |
| D13 | Migration de lignes anciennes : octets/digests/signatures/générations inchangés, précision de source conservée et lignes ambiguës isolées. | C04/C18/C22. |
| D14 | Producteurs/consommateurs mixtes et clé d'idempotence commune v1/v2 : sélection explicite, conflit au contenu divergent et aucun repli silencieux. | C05/C20/C21/C27. |
| D15 | Bascule, retrait v1 et restauration avec données v2 : lecteurs compatibles, mandats courants et absence de transformation destructive. | C20/C22/C24/C27. |
| D16 | Revue des preuves et des profils sélectionnés : aucune compatibilité ni recette intégrée déduite de la seule validation documentaire. | C28 ; A5. |

L'exécution éventuelle utilisera données et ressources de test isolées,
mandats d'effet propres et fournisseurs réels quand leur garantie est visée.
Les durées, tailles et profils réels proviendront de leurs sources validées.
La présente demande n'exécute ni migration PostgreSQL, ni compilation, ni
test produit, ni accès à un secret ou à un environnement partagé.

## 8. Décisions détaillées adoptées et état résultant

| Décision validée | Contenu adopté | Ce qui reste ensuite à produire |
| --- | --- | --- |
| D-A1 | Modèle privé fermé AgentPaBinding 1.0.0, séparation MUTATION/READ, immutabilité, révisions et cycle de liaison ci-dessus. | S1/R1/F1 arrêtent les choix complémentaires ; schémas exacts, intégration, fournisseurs exécutables, réalisation et preuves restent à produire. |
| D-A2 | Transitions natives, projection conditionnelle et règles de refus/réconciliation décrites au §4. | Interfaces concrètes de lecture et déduplication des faits rapprochées avec PA01/PA10, puis réalisation et qualification. |
| D-A3 | Contrats Agent 2.0.0 à grammaire UTC six décimales, champs non temporels conservés et définition canonique de contenu v2 distincte du §5.2. | Descripteurs et consommateurs, réalisation du codec/validateurs sous autorisation distincte et preuves. |
| D-MIG | Migration additive M0–M5, historique intact, idempotence commune et retour arrière sans perte de précision ni destruction. | S1 retient les tables privées et provenance distincte ; schéma exact, plan de migration/retour exécutable et preuves restent à produire. |

Les orientations A1–A5 restent **VALIDÉES ET CANONIQUES**. Les détails D-A1,
D-A2, D-A3 et D-MIG sont **VALIDÉS DOCUMENTAIREMENT**, inscrits dans les
deltas PA01 et **SYNCHRONISÉS AU CANON PIXS-AGENT** sur demande explicite
complémentaire du développeur le 26 octobre 2026.
La version Agent 2.0.0 reste **NON LIVRÉE** et la migration **NON EXÉCUTÉE**.
Aucune tâche de réalisation n'est
cochée. Le blocage fonctionnel persiste tant que contrats exécutables,
fournisseurs, exécutables et preuves nécessaires ne sont pas disponibles.
