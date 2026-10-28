## ADDED Requirements

### Requirement: Dernière stable Cython au début de chaque campagne PA01

Au début de chaque campagne de qualification PA01, la chaîne MUST sélectionner la dernière version stable de Cython publiée et non retirée sur la source officielle PyPI à la date de vérification. Les préversions et versions de développement MUST NOT être sélectionnées comme dernière stable. La sélection MUST être réévaluée à chaque nouvelle campagne.

#### Scenario: Sélection de la dernière stable au début de la campagne

- **WHEN** une nouvelle campagne PA01 commence et PyPI publie une version stable plus récente que le verrou précédent, ainsi qu'une préversion encore plus récente
- **THEN** la version stable publiée et non retirée la plus récente est sélectionnée, la préversion est exclue et la vérification datée, la source, la version et les éléments de provenance et d'intégrité sont enregistrés avec le verrou de la campagne

### Requirement: Traçabilité de la chaîne Cython PA01

La date de vérification, la source officielle, la version exacte sélectionnée, la provenance et les empreintes des distributions utilisées MUST être enregistrées avec la chaîne de la campagne. Les preuves historiques MUST rester rattachées à leurs versions et artefacts ; elles MUST NOT être attribuées automatiquement à une nouvelle chaîne.

#### Scenario: Conservation des preuves après changement de version

- **WHEN** une campagne utilise une version Cython différente d'une campagne antérieure
- **THEN** chaque campagne conserve sa vérification datée, sa source, sa version, sa provenance et ses empreintes, et les anciennes preuves restent liées à leurs versions et artefacts d'origine

### Requirement: Verrouillage exact de Cython pendant la campagne PA01

La version exacte sélectionnée MUST être verrouillée dans `toolchain.cython` du profil PA01 pendant la campagne et pour la reproduction de ses artefacts. Les déclarations, métadonnées et contrôles de construction MUST vérifier cette version ; une contrainte ouverte MUST NOT remplacer le verrou. Une nouvelle publication MUST NOT modifier automatiquement la campagne ou ses preuves. La seule reproduction MUST NOT imposer une nouvelle sélection de la dernière stable.

#### Scenario: Publication pendant une campagne et reproduction des artefacts

- **WHEN** une nouvelle stable est publiée après le verrouillage d'une campagne ou qu'un artefact de cette campagne doit être reproduit
- **THEN** la version verrouillée est conservée et une version effective différente est refusée par les contrôles de construction, sans actualisation automatique ni nouvelle sélection pour la seule reproduction

### Requirement: Actualisation coordonnée de Cython pour PA01

Tout changement de version Cython MUST entraîner la mise à jour coordonnée de `pyproject.toml`, des métadonnées de chaîne, des contrôles PA01, des tests concernés et de la documentation courante, puis la qualification de la nouvelle chaîne. La sélection ou l'inscription documentaire d'une version MUST NOT tenir lieu de qualification.

#### Scenario: Actualisation lors de la campagne suivante

- **WHEN** une campagne suivante sélectionne une nouvelle stable Cython
- **THEN** les déclarations, métadonnées de chaîne, contrôles PA01, tests concernés et documentation courante sont alignés avant la qualification de la nouvelle chaîne, tandis que les preuves historiques restent liées à leurs anciens artefacts et versions

### Requirement: Préservation des autres choix de chaîne PA01

La sélection d'une version Cython MUST NOT modifier implicitement CPython, le mode GIL, l'ABI, les cibles ou les autres choix adoptés. La politique de dernière stable MUST NOT valoir autorisation d'installation.

#### Scenario: Nouvelle version Cython avec autres choix conservés

- **WHEN** une nouvelle stable Cython est sélectionnée pour PA01
- **THEN** CPython, le GIL, l'ABI, les cibles et les autres choix adoptés restent conservés, et aucune installation n'est autorisée par la seule sélection

### Requirement: Blocage si la dernière stable Cython ne peut pas être qualifiée

Si la dernière stable ne peut pas être vérifiée ou si sa compatibilité ne peut pas être qualifiée, la sélection ou la qualification concernée MUST rester bloquée. Une ancienne version MUST NOT être choisie implicitement pour contourner ce blocage.

#### Scenario: Dernière stable non vérifiable ou incompatible

- **WHEN** la source officielle ne permet pas de vérifier la dernière stable ou que cette version ne peut pas être qualifiée avec la chaîne et les cibles adoptées
- **THEN** la sélection ou la qualification reste bloquée, sans repli implicite vers une ancienne version ni modification implicite de CPython, du GIL, de l'ABI ou des cibles

### Requirement: Liaison serveur persistante du contexte Agent et PA

En gestion ordinaire, pixs.agent MUST posséder une liaison persistante côté serveur entre opération, cible, scope, génération Agent et références techniques PA/C08, sous contrôle des propriétaires. Une liaison absente, périmée ou divergente MUST être refusée. Une donnée client MUST NOT suffire à établir cette liaison ; les compteurs natifs PA MUST rester distincts de la génération Agent.

#### Scenario: Liaison absente ou divergente

- **WHEN** un résultat technique est présenté sans liaison serveur courante correspondant à son opération, sa cible, son scope et sa génération Agent
- **THEN** son rapprochement avec l'état Agent est refusé sans déduire une génération depuis un compteur natif ou une déclaration cliente

### Requirement: Contexte initial PA distinct de la gestion ordinaire Agent

L'amorçage avant PostgreSQL MUST conserver son contexte initial C08/PA. Il MUST NOT créer une génération Agent fictive pour satisfaire la liaison de gestion ordinaire. La décision de liaison serveur MUST NOT ajouter implicitement de champs aux messages PA existants ; sa structure et ses règles de mise à jour MUST être spécifiées conjointement par PA01/C08/PA10 avant réalisation dépendante.

#### Scenario: Amorçage avant disponibilité du contexte Agent

- **WHEN** C08 et PA exécutent le parcours initial avant PostgreSQL et les autorités Agent requises
- **THEN** ils conservent le contexte initial propriétaire sans fabriquer de génération ou d'autorité Agent

### Requirement: Phases PA et issues Agent séparées avec projection conditionnelle

Les phases techniques PA et les issues de gestion Agent MUST rester distinctes. Toute projection MUST être explicite, conditionnelle et liée aux preuves requises. Son tableau exact de transitions, contrôles et refus MUST être arrêté dans les contrats PA01/PA10 avant branchement ; une égalité de libellé MUST NOT constituer une preuve d'effet ou de confirmation.

#### Scenario: Réception ou progression sans fait appliqué

- **WHEN** la phase native vaut RECEIVED ou RUNNING
- **THEN** aucun état appliqué ni confirmation Agent n'est déduit de la seule réception ou progression

#### Scenario: Succès technique sans confirmation automatique

- **WHEN** la phase native vaut SUCCEEDED et le succès technique durable est vérifié
- **THEN** la confirmation Agent exige encore ses contrôles propres d'origine et de postcondition et n'est pas produite depuis la seule phase native

#### Scenario: Échec connu et issue incertaine distincts

- **WHEN** la phase native vaut FAILED ou IN_DOUBT
- **THEN** le rapprochement conserve respectivement l'échec connu ou l'incertitude sous preuves propriétaires, et IN_DOUBT exige une réconciliation avant nouvel effet

#### Scenario: Précondition refusée sans échec d'exécution fabriqué

- **WHEN** la phase native vaut BLOCKED
- **THEN** le refus de précondition reste explicite et ne produit pas de constat fictif d'exécution échouée

### Requirement: Évolution versionnée de la précision temporelle Agent

La frontière Agent MUST évoluer par une nouvelle version acceptant les six décimales natives. Le contrat Agent 1.0.0 MUST rester inchangé jusqu'à une migration explicitement définie. Le numéro, le schéma exact, la compatibilité des consommateurs et la migration des états persistés MUST être spécifiés avant leur réalisation ; l'adoption du principe MUST NOT rendre la nouvelle version disponible.

#### Scenario: Principe temporel adopté avant migration

- **WHEN** l'évolution temporelle Agent est adoptée mais sa nouvelle version et sa migration ne sont pas encore spécifiées et livrées
- **THEN** le contrat 1.0.0 reste inchangé et aucune compatibilité avec les dates natives fractionnaires n'est déclarée réalisée

### Requirement: Conservation des instants exacts et des preuves temporelles signées

Les octets signés et les preuves d'origine MUST rester intacts. Les contrôles temporels MUST utiliser l'instant exact et les preuves du fournisseur compétent. Un affichage moins précis MUST NOT participer aux décisions de sécurité ; arrondi ou troncature MUST NOT remplacer l'instant de contrôle. Cette décision MUST NOT sélectionner un nouveau délai, seuil ou producteur concret.

#### Scenario: Affichage à précision réduite

- **WHEN** une interface affiche à la seconde un instant natif à six décimales
- **THEN** les preuves signées restent intactes et les contrôles utilisent l'instant exact et le fournisseur temporel compétent

### Requirement: Qualification progressive PA PZT et recette intégrée obligatoire

La qualification PA/PZT MUST distinguer chaîne Cython/constructeur/liaison, véritables exécutables, parcours intégré réel, puis distributions et plateformes sélectionnées. Une recette intégrée MUST rester obligatoire ; une réussite partielle MUST NOT clôturer cette recette ni qualifier une autre plateforme. Les cas applicables C01–C28 et R01–R68 MUST rester couverts par leurs preuves.

#### Scenario: Construction réussie avant exécutables fonctionnels

- **WHEN** seule la chaîne de construction et de liaison dispose de preuves sur des fixtures
- **THEN** ce palier garde sa portée et les exécutables fonctionnels ainsi que la recette intégrée restent non qualifiés

### Requirement: Revue explicite des preuves avant promotion PA PZT

Chaque résultat de qualification MUST rester lié aux sources, versions, empreintes, commandes exécutées, postconditions et nettoyage. La promotion MUST être précédée d'une revue explicite des preuves réelles. L'adoption documentaire A1–A5 MUST NOT tenir lieu de raccordement livré, de fournisseur concret, de nouvelle preuve fonctionnelle ou d'autorisation de réalisation.

#### Scenario: Décisions adoptées et preuves encore manquantes

- **WHEN** A1–A5 sont validés mais que les fournisseurs, exécutables ou preuves intégrées applicables manquent
- **THEN** les choix sont déclarés adoptés tandis que la qualification fonctionnelle reste bloquée sans promotion ni nouvelle tâche cochée

### Requirement: Métadonnées fermées et identité de campagne PA01

L'enveloppe TOML PA01 MUST avoir les seules racines `schema_version`, `campaign`, `toolchain`, `selection`, `distributions`. Le schéma MUST être `1.0.0` ; campaign MUST contenir seulement un `id` unique non vide et `component=pa01`, toolchain seulement `cython`, version stable exacte normalisée. Les tables MUST être fermées ; champs inconnus, absents, dupliqués ou mal typés MUST être refusés. L'identité et les entrées figées MUST être conservées pour reproduire la campagne.

#### Scenario: Métadonnées valides et reproduction

- **WHEN** une campagne fournit les métadonnées fermées valides et qu'une reproduction est ensuite demandée
- **THEN** le même identifiant, le verrou et les preuves figées sont conservés, sans nouvelle sélection de version ni réécriture des métadonnées historiques

#### Scenario: Métadonnées invalides

- **WHEN** un champ est absent, inconnu, dupliqué ou mal typé, ou que le verrou contient une contrainte ouverte, une préversion, une version de développement, locale ou non normalisée
- **THEN** les métadonnées sont refusées avant compilation avec PA01_CAMPAIGN_METADATA_INVALID, sans valeur implicite ni correction automatique

### Requirement: Preuve de sélection Cython dans la campagne PA01

La table selection MUST contenir seulement `verified_at` UTC textuel, `source_url` PyPI officiel, `snapshot` relatif au document et `snapshot_sha256`. Le relevé JSON conservé MUST prouver la dernière stable non retirée à cette date ; son empreinte MUST être vérifiée sur ses octets. Un chemin sortant ou symbolique MUST être refusé. Une empreinte seule MUST NOT prouver l'origine officielle. Le constructeur MUST utiliser la sélection vérifiée, sans consulter PyPI ni choisir une version.

#### Scenario: Relevé absent ou preuve non concluante

- **WHEN** la date ou la source est invalide, le relevé est absent, sortant, symbolique ou altéré, ou qu'il ne démontre pas la sélection officielle de la dernière stable non retirée
- **THEN** la sélection ou la construction reste bloquée avec PA01_CAMPAIGN_EVIDENCE_INVALID pour une preuve inexploitable, sans ancien compilateur choisi implicitement ; un schéma invalide conserve PA01_CAMPAIGN_METADATA_INVALID

### Requirement: Distributions Cython tracées par campagne PA01

distributions MUST être une liste non vide de tables contenant seulement `filename`, `url`, `sha256`. Les noms simples MUST être uniques, les URL HTTPS sans authentification et les SHA-256 en hexadécimal minuscule sur 64 caractères. Chaque fichier utilisé MUST correspondre au nom, à l'URL et au condensat d'une distribution non retirée de la version verrouillée dans le relevé officiel. Une distribution absente ou altérée MUST être refusée avant compilation.

#### Scenario: Distribution non déclarée ou altérée

- **WHEN** un fichier utilisé ne figure pas dans les métadonnées ou que son nom, son URL, son empreinte réelle ou son état dans le relevé officiel ne correspond pas à la distribution autorisée
- **THEN** le contrôle refuse la construction avec PA01_CAMPAIGN_EVIDENCE_INVALID avant compilation, sans téléchargement ou installation implicite

### Requirement: Rapport de construction lié au verrou Cython PA01

Avant compilation, le constructeur MUST rapprocher `toolchain.cython` du profil, sa copie dans l'enveloppe, la déclaration Cython exacte de `pyproject.toml` et la sonde réelle. `build-report.json` MUST conserver `profile_sha256`, `cython_version` avec `locked` et `observed`, et ajouter `campaign_id`, `campaign_metadata_sha256`, distributions vérifiées et issue du contrôle. Les empreintes MUST porter sur les entrées réelles indépendantes du rapport, sans auto-condensat.

#### Scenario: Sonde conforme et rapport lié aux entrées

- **WHEN** le verrou du profil, sa copie dans l'enveloppe, la déclaration et la version observée concordent et que les entrées et distributions ont été vérifiées
- **THEN** le rapport lie l'identifiant, les empreintes des métadonnées et du profil effectifs, les versions verrouillée et observée ainsi que les distributions vérifiées, sans que ce contrôle seul qualifie le binaire

#### Scenario: Sonde inexploitable ou divergence de version

- **WHEN** la sonde est absente, mal typée ou ambiguë, ou que la copie d'enveloppe, la version déclarée ou observée diffère du verrou du profil
- **THEN** le constructeur refuse avant compilation avec PA01_BUILD_CYTHON_METADATA_INVALID pour la sonde ou PA01_BUILD_CYTHON_MISMATCH pour l'écart ; le rapport conserve les valeurs vérifiées et observed vaut null si aucune version exploitable n'est obtenue

### Requirement: Propriété de la liaison privée AgentPaBinding 1.0.0

AgentPaBinding 1.0.0 MUST respecter la propriété et les limites du contrat détaillé D-A1 ci-dessous. La liaison MUST NOT constituer un mandat ou une autorité durable ; l'amorçage C08/PA avant PostgreSQL MUST rester distinct de la gestion ordinaire.

##### Contrat détaillé validé 3.1

Le modèle retenu est un enregistrement privé `AgentPaBinding`, schéma `1.0.0`, possédé
par Agent dans sa persistance serveur. Il lie un contexte de gestion ordinaire
accepté aux références PA/C08/PZT résolues par leurs propriétaires.
Ce nom ne crée ni contrat public ni capacité ; la forme physique du stockage
reste à arrêter avant une éventuelle migration de données.

La liaison n'est ni un mandat ni une preuve d'autorité durable. Son existence,
son état ACTIVE et son empreinte ne dispensent jamais des gardes courantes
A4 avant effet. Le contexte initial C08/PA avant PostgreSQL reste séparé et
ne reçoit pas de génération Agent artificielle.

#### Scenario: Liaison active sans autorité courante

- **WHEN** une liaison est ACTIVE mais qu'un fournisseur ou mandat requis n'est plus valide
- **THEN** la liaison ne vaut pas autorisation et l'effet concerné reste refusé

### Requirement: Modèle fermé de la liaison privée AgentPaBinding

La liaison et ses objets agent, native et audit MUST respecter exactement les champs, types, origines et couplages du modèle détaillé D-A1 ci-dessous. Champ étranger, référence ambiguë, type incohérent ou valeur de profil absente MUST être refusés. Le raccord MUST NOT créer de champ supplémentaire implicite dans NativeRequest ou NativeResult.

##### Contrat détaillé validé 3.2

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

#### Scenario: Champ ou type de liaison incompatible

- **WHEN** un objet de liaison contient un champ inconnu ou un booléen à la place de sa révision entière
- **THEN** la liaison est refusée sans valeur par défaut ni modification des messages natifs

### Requirement: Acceptation et idempotence de la liaison Agent PA

La création MUTATION ou READ MUST suivre les règles D-A1 détaillées ci-dessous, avec commit local connu et idempotence propriétaire. Un commit ou envoi incertain MUST être réconcilié avant nouvelle émission ; une transaction Agent MUST NOT être présentée comme une transaction distribuée avec PA.

##### Contrat détaillé validé 3.3

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

#### Scenario: Commit ou envoi incertain

- **WHEN** le commit local ou la remise de la demande à PZT reste incertain
- **THEN** la situation est réconciliée chez les propriétaires sans émission déduite de la seule intention persistée

#### Scenario: Lecture sans mutation du souhaité

- **WHEN** une demande READ_RESULT est acceptée sous son autorité de lecture courante
- **THEN** la lecture conserve ses identifiants distincts du sujet et n'incrémente pas la génération du souhaité

#### Scenario: Rejeu identique de liaison

- **WHEN** la même demande déjà acceptée est présentée avec son contexte et son contenu identiques
- **THEN** la liaison et le résultat connus sont retrouvés sans nouvel effet ni génération

### Requirement: Cycle et immutabilité de la liaison Agent PA

Les états PREPARED, ACTIVE, SUSPENDED et RETIRED MUST suivre le cycle D-A1 détaillé ci-dessous. Le payload de rapprochement MUST rester immuable ; les révisions et contrôles courants MUST préserver concurrence, refus, reprise et attribution à la génération d'origine. Un mandat consommé MUST NOT être réutilisé lors d'une reprise.

##### Contrat détaillé validé 3.4

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

#### Scenario: Résultat tardif après changement de génération

- **WHEN** une réponse arrive pour une liaison d'une génération devenue historique
- **THEN** elle reste liée à son opération d'origine et ne remplace pas l'état courant d'une autre génération

#### Scenario: Suspension et issue inconnue

- **WHEN** une liaison est suspendue alors qu'un effet possible n'est pas réconcilié
- **THEN** aucun nouvel effet n'est émis et la suspension ne réactive pas une permission consommée

### Requirement: Résolution privée des preuves de résultat Agent PA

Le reçu privé de résolution MUST respecter les références et garanties D-A1 détaillées ci-dessous. Le fournisseur compétent MUST établir le snapshot courant et son ordre causal ; date, compteur ou référence client MUST NOT fournir cette autorité. Un fournisseur absent MUST bloquer le rapprochement sans ajout implicite aux messages natifs.

##### Contrat détaillé validé 3.5

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

#### Scenario: Ordre de résultat sans preuve propriétaire

- **WHEN** deux notifications ne disposent pas d'une résolution propriétaire courante de leur ordre causal
- **THEN** leur date ou compteur client ne décide pas de la progression et le rapprochement reste bloqué

### Requirement: Transitions natives détaillées du raccord Agent PA

Les phases d'une invocation native MUST suivre la table D-A2 détaillée ci-dessous. Le consommateur MUST résoudre un snapshot courant sans fabriquer les événements intermédiaires non observés. Une issue incertaine MUST rester IN_DOUBT jusqu'à réconciliation ; un résultat terminal contradictoire MUST être traité comme divergence.

##### Contrat détaillé validé 4.1

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

#### Scenario: Effet possible et issue inconnue

- **WHEN** un traitement RUNNING ne peut plus établir l'issue d'un effet possible
- **THEN** il conserve IN_DOUBT sans fabriquer FAILED ou BLOCKED et sans rejeu automatique

#### Scenario: Instantané sans observation de chaque phase

- **WHEN** une première lecture autorisée obtient un résultat terminal propriétaire courant
- **THEN** le consommateur peut le rapprocher sous preuves sans inventer une suite d'événements intermédiaires reçus

#### Scenario: Lecture réussie et effet du sujet distincts

- **WHEN** READ_RESULT réussit à lire un résultat d'une autre opération
- **THEN** son succès de lecture ne confirme pas l'effet de l'opération lue

### Requirement: Projection détaillée des phases PA vers les issues Agent

La projection MUST respecter la table et les distinctions D-A2 détaillées ci-dessous. RECEIVED/RUNNING MUST NOT produire une application ; SUCCEEDED MUST NOT confirmer Agent sans contrôles d'origine et de postcondition. unknown MUST conserver origin_proof absent dans le résultat Agent, sans effacer les preuves natives séparées.

##### Contrat détaillé validé 4.2

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

#### Scenario: Confirmation séparée du succès technique

- **WHEN** un succès technique existe sans confirmation Agent et postcondition vérifiées
- **THEN** aucun résultat confirmed ni fait CONFIRMED n'est fabriqué

#### Scenario: Incertitude et preuve native conservée

- **WHEN** une issue de gestion unknown est produite dans son contexte autorisé
- **THEN** origin_proof reste absent du résultat Agent et les preuves natives de réconciliation sont conservées séparément

#### Scenario: Précondition bloquée sans exécution fictive

- **WHEN** la phase native vaut BLOCKED
- **THEN** un refus typé est conservé sans résultat failed d'exécution ou document appliqué fabriqué

### Requirement: Refus et réordonnancement des observations Agent PA

Le rapprochement MUST appliquer les règles D-A2 détaillées ci-dessous pour refus, doublons et réordonnancement. Il MUST préserver l'identité, le contexte et la preuve causale courante, sans régression d'une observation confirmée ni deuxième effet. Une ancienne confirmation MUST NOT devenir courante sans les contrôles requis.

##### Contrat détaillé validé 4.3

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

#### Scenario: Notification dupliquée ou ancienne

- **WHEN** une notification répétée ou antérieure est reçue après une observation confirmée
- **THEN** la preuve immuable et l'état propriétaire sont rapprochés sans nouvel effet ni régression de l'état courant

### Requirement: Contrats temporels Agent 2.0.0

La nouvelle frontière Agent MUST utiliser la version exacte 2.0.0 et les identifiants, formes fermées, champs temporels et règles D-A3 détaillés ci-dessous. La sélection MUST être explicite par composition et compatibilité, sans déduction depuis la forme d'une date. Le contrat 1.0.0 MUST rester distinct et inchangé jusqu'à la migration définie.

##### Contrat détaillé validé 5.1

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

#### Scenario: Sélection explicite du contrat temporel

- **WHEN** un consommateur est sélectionné pour les contrats Agent 2.0.0
- **THEN** les dates UTC à six décimales sont validées exactement et une date v1 n'est pas acceptée par détection ou normalisation implicite

#### Scenario: Précision textuelle sans autorité temporelle

- **WHEN** un message contient six décimales mais aucune preuve temporelle compétente requise
- **THEN** la précision de représentation ne vaut pas synchronisation ni autorisation et l'usage protégé reste refusé

### Requirement: Codec de contenu Agent v2 et intégrité des contenus v1

Le contenu Agent 2.0.0 MUST utiliser agent-content.v2 et la forme canonique D-A3 détaillée ci-dessous. Les domaines agent-head.v1 et agent-idem.v1 MUST être conservés s'ils restent inchangés. Contenus, signatures, digests et clés historiques MUST NOT être réécrits ou recalculés comme v2 ; les engagements E4/E5 MUST rester natifs.

##### Contrat détaillé validé 5.2

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

#### Scenario: Historique v1 et nouveau contenu v2

- **WHEN** un contenu Agent v2 est créé ou un ancien contenu v1 est relu
- **THEN** le codec approprié est sélectionné et les octets ainsi que les digests historiques et natifs restent intacts

### Requirement: Provenance des données lors de la migration temporelle Agent

La migration MUST suivre les règles de données et de compatibilité D-MIG détaillées ci-dessous. payload_contract_version et la provenance MUST distinguer les versions sans les deviner depuis une date. Une ligne ambiguë MUST bloquer son usage protégé ; une vue à zéros fractionnaires MUST NOT augmenter la précision de source ou réécrire l'historique.

##### Contrat détaillé validé 6.1

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

#### Scenario: Donnée ancienne sans provenance suffisante

- **WHEN** un fait ancien ne peut pas être classifié avec sa provenance et son codec
- **THEN** il n'est pas interprété comme v2 et son usage protégé reste bloqué

#### Scenario: Vue de lecture d'un instant ancien

- **WHEN** une date v1 est affichée par une vue comportant des zéros fractionnaires
- **THEN** le stockage et son digest restent inchangés et la précision de source ne devient pas microseconde

### Requirement: Étapes additives de migration Agent M0 à M5

La migration MUST suivre les étapes et conditions de passage M0–M5 détaillées ci-dessous. La coexistence et la bascule MUST dépendre des preuves et profils sélectionnés, sans délai implicite. Une opération IN_DOUBT MUST NOT être relancée ou effacée pour achever le retrait des écritures v1 ; le plan physique et l'exécution MUST rester distincts de son adoption.

##### Contrat détaillé validé 6.2

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

#### Scenario: Activation de nouvelles écritures v2

- **WHEN** le passage à M4 est demandé
- **THEN** les fournisseurs, consommateurs, gardes et preuves du périmètre sont vérifiés avant activation effective

#### Scenario: Retrait v1 avec opération incertaine

- **WHEN** une opération v1 reste IN_DOUBT au moment du passage à M5
- **THEN** elle est réconciliée ou conservée dans un parcours isolé supporté sans rejeu ni effacement pour terminer la migration

### Requirement: Idempotence entre versions Agent 1 et 2

Les rejeux entre versions MUST respecter D-MIG ci-dessous. Une opération acceptée en v1 MUST conserver ses octets, son codec et sa liaison. Le même contexte d'idempotence MUST NOT créer un deuxième effet sous v2 ; un contenu divergent MUST être refusé sans équivalence supposée depuis une conversion temporelle.

##### Contrat détaillé validé 6.3

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

#### Scenario: Même clé entre versions et contenu divergent

- **WHEN** une demande v2 réutilise l'identité d'idempotence d'une opération v1 avec un contenu différent
- **THEN** le conflit est signalé et la version ne crée pas une nouvelle opération ni un second effet

### Requirement: Retour arrière sans perte temporelle ni restauration d'autorité

Le retour arrière et la restauration MUST respecter D-MIG détaillé ci-dessous. Après écritures v2, un lecteur v2 compatible MUST être conservé ou le périmètre bloqué. La restauration MUST NOT supprimer les nouvelles données, tronquer leur précision, réécrire l'historique ou réactiver une génération ou un mandat révoqué.

##### Contrat détaillé validé 6.4

Avant toute écriture v2, le retour peut retirer sa sélection et conserver
les données originales intactes. Après des écritures v2, garder un lecteur
v2 compatible ou bloquer le périmètre : un ancien binaire incapable de lire
ces données ne les convertit pas automatiquement à la seconde.

Ne pas supprimer les nouvelles données, réécrire l'historique, restaurer
une ancienne génération ou réactiver un mandat révoqué pour revenir en v1.
Une restauration rapproche versions, révocations et opérations incertaines
avec les propriétaires courants avant reprise. Les migrations descendantes
destructives et transformations de signatures sont exclues de cette stratégie validée.

#### Scenario: Retour après des écritures v2

- **WHEN** un retour vers un ancien composant incapable de lire les données v2 est demandé
- **THEN** un lecteur compatible est conservé ou le périmètre reste bloqué sans conversion automatique à la seconde

#### Scenario: Restauration et autorité courante

- **WHEN** des données sont restaurées après évolution des versions ou révocations
- **THEN** les propriétaires courants sont rapprochés et aucun ancien droit ou mandat révoqué n'est réactivé


### Requirement: Admission indépendante de la sélection officielle Cython PA01

La sélection Cython PA01 MUST provenir d'une observation directe HTTPS vérifiée et datée en UTC, suivie d'une revue explicitement autorisée du dossier figé. L'admission MUST lier le manifeste exact et la campagne dans un registre protégé distinct du candidat, non modifiable par le constructeur ou son appelant. Un booléen, un relevé auto-déclaré ou son empreinte seule MUST NOT établir cette autorité. Le constructeur MUST vérifier l'admission hors ligne.

#### Scenario: Observation et revue du manifeste exact

- **WHEN** une nouvelle campagne dispose d'une observation officielle exploitable, d'une sélection de la dernière stable non retirée, d'entrées figées vérifiées et d'une revue explicitement autorisée
- **THEN** une admission liée à l'identité de campagne et au manifeste exact est conservée dans le registre protégé, sans que cette décision seule autorise installation, compilation ou qualification

#### Scenario: Preuve auto-déclarée ou registre substitué

- **WHEN** le demandeur fournit un booléen de validation, une admission dans son candidat, une identité de responsable non autorisée ou un registre de remplacement
- **THEN** ces éléments ne valent pas admission et le contrôle refuse avant outils avec PA01_CAMPAIGN_EVIDENCE_INVALID, sans repli implicite ni compilation

#### Scenario: Observation officielle impossible ou non concluante

- **WHEN** HTTPS ou la date n'est pas vérifiable, la source est indisponible ou différente, ou que les données ne permettent pas d'établir la dernière stable non retirée
- **THEN** aucune sélection n'est admise, aucune preuve rétroactive n'est inventée et aucune ancienne version n'est choisie implicitement

### Requirement: Conservation et rattachement des preuves de sélection PA01

Le dossier figé MUST conserver entrées, manifeste, autorisation et admission sans réécriture. Le registre MUST préserver retraits et état courant ; une admission absente, retirée ou invérifiable MUST bloquer la construction. Le rapport MUST lier `selection_admission_ref`, `selection_admission_sha256` et `selection_manifest_sha256` aux preuves vérifiées, sans cycle d'empreintes. La reproduction MUST conserver dates et entrées sans nouvelle sélection.

#### Scenario: Altération ou échange après admission

- **WHEN** un fichier ou le manifeste est altéré, ou qu'une admission est présentée pour une autre campagne ou d'autres octets
- **THEN** les empreintes ou l'identité divergent, la construction est refusée avec PA01_CAMPAIGN_EVIDENCE_INVALID et les preuves d'origine restent conservées

#### Scenario: Retrait ou état courant non vérifiable

- **WHEN** l'admission est absente, retirée, inaccessible ou que son état courant est ambigu, y compris après restauration
- **THEN** la construction reste bloquée avec PA01_CAMPAIGN_EVIDENCE_INVALID, sans réactivation depuis une ancienne copie favorable

#### Scenario: Reproduction avec admission et rapport liés

- **WHEN** les entrées et l'admission de la campagne d'origine restent vérifiées et utilisables pour une reproduction
- **THEN** dates et versions d'origine sont conservées, le rapport lie les références et empreintes vérifiées d'admission et de manifeste, et le constructeur ne consulte pas PyPI pour sélectionner une autre version


### Requirement: Stockage PostgreSQL privé dédié aux liaisons et remises Agent

Agent MUST utiliser des tables PostgreSQL privées dédiées pour liaison/révisions, intentions/tentatives de remise et version/provenance historique, selon S1. Elles MUST préserver identité, scope, génération, révision, payload immuable et octets engagés exacts. La migration MUST rester additive selon D-MIG. Une projection JSONB MUST NOT remplacer les octets signés ou hachés.

##### Contrat détaillé validé S1

| Élément | Règle validée |
| --- | --- |
| Propriété | Dépôt Agent via Django/PostgreSQL ; même base et transaction propriétaire que l'opération concernée. |
| Forme physique retenue | Tables privées dédiées pour AgentPaBinding 1.0.0 et historique de révisions, intentions durables de remise à PZT et tentatives, version/provenance distinctes des payloads historiques. |
| Intégrité | Colonnes typées et contraintes explicites pour identité, scope, génération et révision ; noms exacts, contraintes et modèles restent à détailler puis réaliser. |
| Immutabilité | Payload de rapprochement immuable séparé de l'état courant et de sa révision contrôlée ; cycle D-A1 conservé, sans assimilation aux générations Agent ou compteurs PA. |
| Documents engagés | Octets exacts des documents non secrets conservés ; projection JSONB de recherche possible sans substitution au codec ou aux octets d'origine ; preuves natives chez leurs propriétaires. |
| Migration | Extension additive M0–M5, version et provenance explicites ; historique, identités, générations, signatures, digests et précision de source conservés. Aucun DDL ou migration exécuté par cette adoption. |

#### Scenario: Persistance et conflit de révision

- **WHEN** une liaison est persistée ou son état courant est révisé
- **THEN** les contraintes privées préservent identité, scope et génération, le payload de rapprochement reste immuable et une révision divergente ne réaffecte pas la liaison

#### Scenario: Projection JSONB et preuve engagée

- **WHEN** une projection de recherche diffère de la représentation originale d'un document signé ou haché
- **THEN** les octets exacts et le codec propriétaire restent la référence engagée et la projection ne remplace pas la preuve

#### Scenario: Extension du stockage historique

- **WHEN** la migration additive enrichit les versions et provenances des payloads historiques
- **THEN** les anciennes données engagées restent intactes et une provenance ambiguë bloque l'usage protégé sans réécriture pour lever l'ambiguïté

### Requirement: Outbox Agent transactionnelle et relais PBO vers PZT

Agent MUST persister opération MUTATION, liaison et intention de remise dans la même transaction locale propriétaire. Le relais PBO MUST soumettre l'intention via PZT seulement après commit vérifié, sans broker externe. Cette atomicité MUST NOT être présentée comme une transaction distribuée ou une preuve de remise. READ MUST conserver la séparation D-A1 sans incrément du souhaité.

##### Contrat détaillé validé R1 — remise

| Élément | Règle validée |
| --- | --- |
| Mécanisme | Outbox durable privée Agent et relais dans PBO vers l'adaptateur PZT ; pas de canal direct PBO–PA. |
| Frontière transactionnelle | Opération MUTATION, liaison et intention atomiques dans la même base propriétaire ; émission réseau après commit local vérifié seulement. |
| Incertitude du commit | Réconciliation du résultat local avant remise ; l'intention seule ne prouve ni commit acquis, ni livraison, ni absence d'effet distant. |
| Réutilisation C09 | Réutiliser des mécanismes compatibles par une frontière d'intégration explicitement définie ; le participant C09 des mutations Core n'est pas un raccord Agent directement utilisable et ne justifie aucune dépendance privée. |
| Livraison restante | Schéma, interface d'intégration, relais, concurrence, reprise et diagnostics restent à préciser puis réaliser et qualifier ; aucun nouveau statut public ou calendrier de tentative n'est fixé. |

#### Scenario: Commit vérifié avant remise

- **WHEN** une mutation Agent est acceptée puis son commit local est vérifié
- **THEN** opération, liaison et intention sont persistées atomiquement et le relais peut seulement ensuite soumettre la demande à PZT sous les contrôles courants

#### Scenario: Rollback ou commit incertain

- **WHEN** la transaction est annulée ou son issue n'est pas établie
- **THEN** aucun envoi n'est déclenché sur l'intention seule et une issue incertaine est réconciliée avant toute remise

### Requirement: Recontrôle et réconciliation des tentatives de remise Agent

Avant émission ou reprise, le relais Agent MUST recontrôler génération, état de liaison, mandat, expiration, relation et identité attendue. Une issue d'envoi incertaine MUST être réconciliée avant réémission, sans permission consommée rejouée. Un ACK PZT MUST NOT valoir succès PA ou confirmation Agent. La remise répétée MUST NOT suffire à garantir l'absence de double effet natif.

##### Contrat détaillé validé R1 — reprise

| Élément | Règle validée |
| --- | --- |
| Contrôle courant | Sources propriétaires compétentes pour chaque garde, sans remplacement des contrôles PZT/PA au point d'usage avant effet. |
| Trace durable | Intentions, tentatives et résultats connus conservés ; incertitude distincte d'un échec connu ou d'une absence d'effet prouvée. |
| Réconciliation | Rapprocher les états propriétaires avant réémission lorsque l'issue est inconnue ; ne pas recycler un mandat consommé. |
| Réception et effet | ACK limité à la réception de son contrat ; succès technique, observation, postcondition et confirmation restent distincts selon D-A2. |
| Double effet | Idempotence, journal et réconciliation natifs nécessaires au-delà du mécanisme de remise ; aucune garantie déduite de la seule répétition de livraison. |

#### Scenario: Contexte changé avant reprise

- **WHEN** une tentative reprend avec génération, liaison, mandat, expiration, relation ou identité devenue invalide
- **THEN** l'émission est refusée sur le contexte courant sans réutilisation d'une ancienne vérification favorable ou permission consommée

#### Scenario: Réponse perdue ou ACK reçu seul

- **WHEN** l'issue d'envoi est inconnue ou qu'un ACK PZT constitue le seul retour
- **THEN** aucun succès PA ni confirmation Agent n'est fabriqué, l'incertitude requise est conservée et une réémission éventuelle attend la réconciliation et les garanties natives applicables

### Requirement: Fournisseurs PA PZT retenus et disponibilité démontrée

La composition MUST sélectionner les fournisseurs F1 par responsabilité, avec implémentation exécutable, version, propriétaire et preuves applicables. Le temps MUST provenir des producteurs propres aux processus PBO/PA/PZT derrière TimeProducer 2.0.0. Un fournisseur requis absent, ambigu ou sans preuve courante MUST bloquer l'usage protégé. Une sélection documentaire MUST NOT valoir livraison ou qualification.

##### Contrat détaillé validé F1

| Besoin | Fournisseur ou mécanisme retenu et limite |
| --- | --- |
| Liaison et provenance | Dépôt privé Agent Django/PostgreSQL selon S1 ; modèles, contraintes, migration et preuves restent à produire. |
| Remise et transport | Outbox/relais Agent PBO selon R1 vers adaptateur PZT ; E3 local conserve l'adaptateur Cython/OpenSSL 3 mTLS adopté. Relais, client/serveur, admission et routage réels restent à livrer. |
| Mandats et autorisation | Fournisseurs des contrats publics Core/Auth pour gestion ordinaire ; fournisseurs PA/C08/Z12 du parcours initial ; aucune autorité Core fictive avant PostgreSQL. |
| Résultat technique | Résolveur natif PA adossé au résultat durable, journal/ancre et postconditions réelles ; codec ou ancre seuls ne prouvent pas l'effet PostgreSQL. |
| Origine et confirmation | Adaptateurs AgentOriginTrustPort et AgentConfirmationTrustPort consommant les preuves propriétaires ; résolution, bindings et vérifications réels encore nécessaires, sans confirmation automatique depuis SUCCEEDED. |
| Temps | Producteurs de chaque processus PBO/PA/PZT enregistrés par composition authentique derrière TimeProducer 2.0.0, sources du profil adopté et acquisition courante. Aucun repli implicite Clock.now ni transfert de garde native en autorisation Python réutilisable. |
| Preuve de disponibilité | Identifier implémentation, version, sélection authentique et preuves de fonctionnement, reprise et révocation ; DTO, Protocol, bibliothèque, symbole ou source seuls insuffisants. Aucun endpoint, compte, port, budget ou seuil supplémentaire sélectionné ici. |

#### Scenario: Interface présente et fournisseur requis absent

- **WHEN** la composition présente un port ou une bibliothèque mais ne peut établir son fournisseur exécutable requis et sa sélection authentique
- **THEN** le parcours protégé reste bloqué sans disponibilité déduite de l'interface ou de la décision F1

#### Scenario: Résultat natif sans postcondition vérifiée

- **WHEN** un résultat, un codec ou une ancre est disponible sans preuve d'origine et de postcondition réelle requise
- **THEN** aucun effet PostgreSQL ni confirmation Agent n'est déduit et les preuves manquantes restent explicitement signalées

#### Scenario: Producteur temporel manquant dans un processus

- **WHEN** un processus PBO, PA ou PZT ne dispose pas de son producteur sélectionné ou de la preuve courante requise au point d'usage
- **THEN** l'usage protégé est refusé sans horloge implicite de remplacement ni garde native transférée comme permission réutilisable

### Requirement: Schéma physique privé Agent validé D S1

Agent MUST appliquer le schéma physique D-S1 : huit tables privées dans la base propriétaire, types et bornes explicites, métadonnées de gouvernance et suppression protégée. Les champs temporels engagés MUST rester distincts des horodatages de suivi. Un identifiant ou une valeur locale MUST NOT valoir autorité.

##### Contrat détaillé validé 3.1–3.2

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

#### Scenario: Huit tables et portée propriétaire

- **WHEN** le stockage D-S1 est préparé ou réalisé
- **THEN** les huit tables et leurs clés suivent le contrat validé, sans base séparée, cascade destructive ou lecture autorisée par le seul identifiant

#### Scenario: Compteur saturé ou gouvernance inconnue

- **WHEN** un compteur atteint sa borne ou la classification de gouvernance est inconnue
- **THEN** le dépassement est refusé et l'inconnu reste restrictif sans rebouclage, classification publique ou durée implicite

### Requirement: Colonnes immuables du binding Agent validées D S1

Le binding Agent MUST suivre les colonnes, types, nullabilités et correspondances D-S1 ci-dessous. MUTATION MUST référencer l'opération et la tête réelles ; READ MUST conserver son contexte sans génération fabriquée. Les projections physiques MUST NOT étendre le modèle logique fermé ou les messages PA.

##### Contrat détaillé validé 3.3

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

#### Scenario: Binding mutation et références réelles

- **WHEN** une liaison MUTATION est créée
- **THEN** opération, tête, scope, acteur, versions, générations et documents correspondent aux sources propriétaires et aucune projection physique n'est ajoutée au wire

#### Scenario: Lecture sans génération résolue

- **WHEN** une lecture ne dispose pas de source compétente pour bound_generation
- **THEN** le raccord ordinaire reste bloqué sans création de tête ou génération artificielle ni attribution rétroactive au parcours initial

### Requirement: État révision et documents Agent validés D S1

Agent MUST écrire état courant et révision historique atomiquement sous comparaison de révision, en conservant le cycle D-A1. Les documents MUST suivre les codecs privés validés et préserver leurs octets exacts. JSONB MUST NOT remplacer les octets engagés ; les preuves natives et secrets MUST NOT être copiés dans ce stockage.

##### Contrat détaillé validé 3.4

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

#### Scenario: Révision concurrente ou modification du payload

- **WHEN** un état est révisé concurremment ou un ancien payload est modifié par un chemin d'écriture
- **THEN** le dépôt refuse l'écriture divergente et préserve l'historique ainsi que le payload immuable

#### Scenario: Traces et document opaque

- **WHEN** des traces ou un document Agent observé sont conservés
- **THEN** les codecs validés préservent ordre et doublons des listes ou octets opaques exacts sans nouveau canon de signature ni domaine d'idempotence

### Requirement: Persistance des remises et tentatives Agent validée D S1

L'intention, les tentatives et événements Agent MUST utiliser les colonnes et formes D-S1 validées. Une intention MUST conserver sa demande native entre tentatives ; un OWNER_SNAPSHOT MUST être complet. Un callback tardif MUST NOT avancer une génération suivante et l'ordonnancement MUST NOT constituer un droit de remise.

##### Contrat détaillé validé 3.5

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

#### Scenario: Snapshot incomplet et callback tardif

- **WHEN** un retour est incomplet ou appartient à une ancienne tentative
- **THEN** aucun snapshot vérifié ou état courant étranger n'est fabriqué et le retour reste traçable à son origine

#### Scenario: Intention en attente sans échéance du profil

- **WHEN** une intention est PENDING sans next_attempt_at fourni par le profil
- **THEN** la forme validée est refusée et aucun calendrier ou droit de remise n'est déduit d'une valeur implicite

### Requirement: Provenance et inventaire physique Agent validés D S1

La provenance Agent MUST cibler exactement une opération, un fait ou un document et conserver ses classifications par révisions liées. Le classement MUST reposer sur le producteur et le contrat, sans réécrire les payloads. Un codec ou digest d'inventaire MUST NOT établir une signature historique ou payload_contract_version à lui seul.

##### Contrat détaillé validé 3.6

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

#### Scenario: Classification révisée et cible unique

- **WHEN** une provenance est ajoutée ou précisée
- **THEN** une seule cible est liée, l'ancienne classification est conservée et la nouvelle révision est rapprochée sous verrou

#### Scenario: Digest d'inventaire sans provenance de producteur

- **WHEN** un ancien fait possède une empreinte d'inventaire mais pas de provenance de version suffisante
- **THEN** le classement protégé reste ambigu ou invalide sans déduction de version depuis le codec ou les seules fractions temporelles

### Requirement: Contraintes et index physiques Agent validés D S1

Agent MUST appliquer les contraintes, index et contrôles propriétaires D-S1 ci-dessous. L'unicité MUST être suivie d'une comparaison intégrale après digest. Les contrôles intertables et d'autorité MUST NOT être présentés comme garantis par un CHECK de ligne ; la réservation locale MUST rester distincte de l'admission distante.

##### Contrat détaillé validé 3.7

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

#### Scenario: Collision ou double liaison de mutation

- **WHEN** une identité a le même digest avec un contenu divergent ou qu'une opération MUTATION reçoit une seconde liaison
- **THEN** la collision ou le conflit est refusé sans création d'un second effet logique

#### Scenario: Clé optionnelle et contrôle propriétaire

- **WHEN** une unicité concerne une cible optionnelle ou qu'un invariant relie plusieurs propriétaires
- **THEN** les index partiels et contrôles transactionnels validés sont utilisés sans égalité implicite des NULL ni CHECK intertables supposé

### Requirement: Opérations privées du relais Agent validées D R1

Le relais privé AgentRelay 1.0.0 MUST exposer les opérations, entrées et sorties validées D-R1. L'émission MUST attendre le commit propriétaire final établi. Un retour de staging, savepoint ou booléen d'appelant MUST NOT constituer une preuve de commit, remise ou permission. Un doute de commit MUST bloquer l'envoi.

##### Contrat détaillé validé 4.1

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

#### Scenario: Commit externe non établi

- **WHEN** un stage retourne alors que la transaction englobante n'a pas de commit établi
- **THEN** aucune émission ne commence et observe_commit rapproche les lignes attendues depuis la transaction indépendante compétente

#### Scenario: Relecture absente ou réplique substituée

- **WHEN** la ligne attendue est absente temporairement ou qu'une réplique remplace la base primaire attendue
- **THEN** le doute reste bloquant sans preuve de rollback ou de remise déduite de cette observation

### Requirement: Concurrence et séquence du relais Agent validées D R1

Le relais Agent MUST suivre la séquence D-R1 : transaction propriétaire, commit établi, réservation courte, gardes courantes, IO_STARTED durable, transport puis retour contrôlé. Les IO MUST rester hors verrous SQL. Une réservation expirée MUST NOT prouver arrêt du worker ou absence d'effet ; une émission incertaine MUST être réconciliée avant réémission.

##### Contrat détaillé validé 4.2

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

#### Scenario: Notification perdue et reprise concurrente

- **WHEN** la notification postcommit est perdue ou que plusieurs workers inspectent l'intention
- **THEN** l'outbox reste découvrable et une seule réservation locale courante est attribuée sous comparaison de révision

#### Scenario: Ancien worker après IO_STARTED

- **WHEN** un worker perd sa réservation après début possible de l'émission puis revient tardivement
- **THEN** son callback n'avance pas l'état courant et la reprise rapproche les propriétaires sans garantie d'émission unique ou réémission sur seule expiration

### Requirement: Transitions locales du relais Agent validées D R1

L'intention Agent MUST conserver les sept états et transitions D-R1 ci-dessous, distincts de la liaison, des phases PA et des issues Agent. L'annulation MUST exiger une absence d'émission prouvée. Un ACK MUST NOT créer un succès PA ou une confirmation Agent. Un profil de tentative manquant MUST bloquer le démarrage concerné.

##### Contrat détaillé validé 4.3

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

#### Scenario: Réconciliation avant retour en attente

- **WHEN** une intention RECONCILE_REQUIRED est candidate à PENDING
- **THEN** les preuves propriétaires et le droit courant de remise sont établis avant la transition, sans réutilisation de permission consommée

#### Scenario: Reçu ou annulation locale

- **WHEN** un ACK est vérifié ou qu'une annulation est demandée
- **THEN** le reçu arrête les remises automatiques sans confirmer un effet et CANCELLED reste réservé à l'absence d'émission établie

### Requirement: Observations et diagnostics du relais Agent validés D R1

Le relais MUST utiliser TransportObservation 1.0.0 et les motifs privés D-R1 validés. RECEIPT MUST être vérifié ; REFUSED_NO_SUBMISSION MUST concerner l'appel prouvé non soumis. Une rupture après IO, ambiguïté ou retour invérifiable MUST rester UNKNOWN. Ces retours MUST NOT étendre les codes wire, phases PA ou issues Agent.

##### Contrat détaillé validé 4.4

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

#### Scenario: Rupture après début de l'émission

- **WHEN** une rupture, un timeout ou un retour ambigu survient après début possible de l'IO
- **THEN** UNKNOWN est conservé et aucune absence d'effet ou réception vérifiée n'est inventée

#### Scenario: Refus non soumis avec tentative antérieure

- **WHEN** un fournisseur prouve que l'appel courant n'a pas été soumis mais qu'une tentative antérieure reste incertaine
- **THEN** le refus est limité à l'appel courant et l'incertitude antérieure impose toujours son rapprochement

### Requirement: Composition privée des fournisseurs validée D F1

La composition des fournisseurs D-F1 MUST lier les sept champs d'enregistrement validés et vérifier portée, versions et état courant des preuves. Un symbole, qualification_ref ou fournisseur auto-déclaré MUST NOT prouver sa qualification. Les autorisations MUST rester chez leurs propriétaires, sans secret ou handle natif sérialisé.

##### Contrat détaillé validé 5.1

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

#### Scenario: Référence de qualification auto-déclarée

- **WHEN** un fournisseur présente sa propre qualification_ref sans vérification de la source et du périmètre
- **THEN** la composition protégée refuse de le considérer qualifié ou disponible

#### Scenario: Version ou composition substituée

- **WHEN** le fournisseur ou sa version ne correspond pas à la composition authentique sélectionnée
- **THEN** l'usage protégé est bloqué sans remplacement implicite ou délégation de l'autorité au Kernel

### Requirement: Interfaces de stockage autorité et transport validées D F1

Les fournisseurs D-F1 MUST suivre les interfaces privées validées de stockage, relais, autorité et transport. Agent MUST utiliser Core/Auth publics pour la gestion ordinaire et conserver le parcours initial PA/C08/Z12 séparé. Les gardes PZT/PA MUST rester courantes avant effet ; Agent MUST NOT préconsommer un mandat critique PA ou créer un canal direct PBO–PA.

##### Contrat détaillé validé 5.2

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

#### Scenario: Gestion ordinaire et parcours initial

- **WHEN** une demande de gestion ou d'amorçage est préparée
- **THEN** le fournisseur du parcours réel est sélectionné sans identité Core ou génération Agent fictive avant PostgreSQL

#### Scenario: Vérification préalable et garde finale

- **WHEN** Agent a réalisé une vérification préalable mais qu'une condition PZT ou PA change
- **THEN** la garde finale refuse l'effet devenu inadmissible sans considérer le contrôle Agent comme permission stockable ou mandat critique déjà consommé

### Requirement: Résolveur et adaptateurs de confiance validés D F1

Le résolveur et les adaptateurs Agent D-F1 MUST suivre les entrées, sorties et refus validés ci-dessous, avec le reçu D-A1 à neuf champs et les signatures de confiance existantes. L'origine, les postconditions et la confirmation MUST être vérifiées réellement. Les références, dates, phases ou diagnostics seuls MUST NOT valoir autorisation ou ordre causal.

##### Contrat détaillé validé 5.3

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

#### Scenario: Résolution sans origine ou postcondition réelle

- **WHEN** un résultat technique est fourni sans l'origine ou la postcondition réelle requise
- **THEN** l'observation ou confirmation protégée est refusée et aucune phase SUCCEEDED ne crée une confirmation automatique

#### Scenario: Unknown et résultat tardif

- **WHEN** une issue Agent est unknown ou qu'un résultat d'une ancienne génération arrive
- **THEN** origin_proof reste None pour unknown, les preuves natives sont préservées séparément et la génération courante n'est pas réécrite

### Requirement: Interfaces temporelles par processus conservées D F1

PBO, PA et PZT MUST composer leurs producteurs temporels selon D-F1, en conservant les quatre méthodes TimeProducer 2.0.0. Les diagnostics et retours None MUST NOT devenir des permissions réutilisables ou ajouter UTC, bail ou pointeur à TimeDiagnostic. Une horloge de suivi MUST NOT remplacer la garde temporelle courante.

##### Contrat détaillé validé 5.4

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

#### Scenario: Diagnostic réinjecté comme permission

- **WHEN** un consommateur tente de réutiliser TimeDiagnostic ou None sans nouvelle garde courante
- **THEN** l'usage protégé ne reçoit aucune autorisation déduite et appelle le producteur compétent au point d'usage

#### Scenario: Producteur absent ou nouvelle API now

- **WHEN** un processus manque de producteur ou qu'une horloge locale est proposée en remplacement
- **THEN** le parcours protégé reste bloqué sans transformer TimeProducer en API now ou livrer un fournisseur par une façade envisagée

### Requirement: Migration physique et restauration validées D SMIG

La migration Agent MUST suivre le détail D-SMIG M0–M5 : extension, classement, coexistence et activation distincte du relais. Les payloads historiques MUST rester intacts et les faits v2 MUST recevoir leur provenance atomiquement. Une restauration MUST rapprocher les effets et autorités propriétaires avant reprise ; elle MUST NOT réémettre automatiquement des intentions du passé.

##### Contrat détaillé validé 6

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

#### Scenario: Classification et bascule v2

- **WHEN** le classement ou la bascule introduit les nouvelles lectures et écritures
- **THEN** les octets et identités historiques restent intacts, les ambiguïtés bloquent leur usage et les versions sont sélectionnées explicitement avec provenance atomique des faits v2

#### Scenario: Retour ou restauration après émission

- **WHEN** un retour après écritures v2 ou une sauvegarde contenant une intention déjà émise est restauré
- **THEN** les lecteurs compatibles sont conservés ou le périmètre bloqué et journaux, effets et révocations sont rapprochés avant toute reprise

### Requirement: Preuves attendues du détail physique PA PZT

La qualification du détail D-S1/D-R1/D-F1/D-SMIG MUST couvrir les dix-huit repères P-SRF01–P-SRF18 avec leurs preuves et liens aux cas existants. Une adoption documentaire ou fixture MUST NOT devenir une qualification du fournisseur réel. Les cas non exécutés MUST rester signalés comme tels et la politique Cython par campagne MUST être conservée.

##### Contrat détaillé validé 7

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

#### Scenario: Adoption sans exécution produit

- **WHEN** les décisions détaillées sont validées et inscrites sans recette produit
- **THEN** les dix-huit repères restent NON EXÉCUTÉS, aucune tâche de réalisation n'est clôturée et aucune disponibilité fonctionnelle n'est déduite

#### Scenario: Preuve limitée à une fixture

- **WHEN** une preuve utilise un double ou une fixture au lieu du fournisseur dont la garantie est visée
- **THEN** sa portée reste limitée au contrôle testé et la recette intégrée et les preuves réelles demeurent requises

