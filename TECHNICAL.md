# TECHNICAL.md — Pixs

Ce document précise les décisions techniques transverses du projet. Il complète `PROJECT.md` sans remplacer les spécifications OpenSpec, qui définissent les comportements implémentables.

## Convention normative RFC 2119

Les exigences techniques vérifiables sont formulées dans OpenSpec en prose française avec les mots-clés RFC 2119 `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT` et `MAY`, toujours en majuscules. Les clauses `MUST` et `MUST NOT` sont obligatoires ; `SHOULD` et `SHOULD NOT` nécessitent une justification explicite en cas d'écart ; `MAY` désigne une capacité optionnelle. Une négation normative doit utiliser la forme canonique `MUST NOT` ou `SHOULD NOT`, jamais une construction hybride comme `NE MUST` ou `NE SHOULD`. Une formulation française ou en minuscules hors spécification ne possède pas cette force normative.

Les choix de ce document qui deviennent observables, testables ou nécessaires à l'interopérabilité doivent être transférés dans la capacité OpenSpec concernée. Aucun détail technique ne peut affaiblir une exigence RFC 2119 déjà validée.

## 1. Identité numérique

L'identité numérique est le référentiel technique de l'authentification Pixs. Elle est distincte de l'utilisateur, du groupe et du provider d'authentification.

```text
Utilisateur 0..1 ─── 0..1 Identité numérique
Compte de service 1 ─── 1 Identité numérique
```

Contraintes obligatoires :

* une identité numérique est liée à zéro ou un utilisateur ;
* un utilisateur est lié à zéro ou une identité numérique ;
* une identité numérique peut exister sans utilisateur ;
* un utilisateur peut exister sans identité numérique ;
* un compte de service est obligatoirement une identité numérique ;
* une identité numérique peut être un compte de service, mais ce n'est pas obligatoire ;
* une identité numérique porte les méthodes d'authentification et les informations de révocation ;
* une identité numérique peut être utilisée comme `Subject` d'autorisation.

Le lien entre un utilisateur et une identité numérique ne doit pas être déduit d'un identifiant fourni par un provider externe. Il doit être représenté explicitement dans la source de vérité Pixs.

L'assurance est portée par des événements et contextes d'authentification, pas par le seul type de l'identité. Pixs distingue au minimum :

```text
identity_assurance       CLAIMED | VERIFIED | PROOFED
authentication_assurance SINGLE_FACTOR | MULTI_FACTOR | PHISHING_RESISTANT
federation_trust         UNTRUSTED | TRUSTED | STRONGLY_BOUND
```

Ces niveaux sont des sémantiques internes et peuvent être mappés par un provider depuis OIDC, SAML, WebAuthn, mTLS ou un mécanisme local. Un mapping doit déclarer les preuves acceptées, son niveau maximal et ses conditions de validité ; un claim absent, ambigu, expiré ou non vérifiable ne peut pas augmenter l'assurance.

## 2. Types d'identité numérique

Les types prévus sont :

```text
HUMAN      identité associée à une personne
SERVICE    identité utilisée par une application ou un processus
DEVICE     identité portée par un appareil ou équipement
FEDERATED  identité provenant d'un système externe
```

Le type décrit la catégorie fonctionnelle exposée par Pixs. Le mode de provisionnement ou le provider d'authentification ne doit pas être confondu avec le type lorsque la conception détaillée nécessitera plusieurs dimensions.

Une identité numérique devrait également disposer d'un état explicite, au minimum :

```text
ACTIVE
SUSPENDED
REVOKED
EXPIRED
```

Les méthodes d'authentification, identifiants externes, dates d'activation et d'expiration, ainsi que les changements d'état doivent être rattachés à l'identité numérique et auditables.

## 3. Frontières de responsabilité

```text
Utilisateur
  └── données de personne ou de contexte métier

Identité numérique
  ├── authentification
  ├── sessions et tokens
  ├── méthodes d'authentification
  ├── révocation et cycle de vie
  └── sujet d'autorisation possible

Provider d'authentification
  └── vérification ou établissement de l'authentification
```

Un provider OIDC, SAML, LDAP ou local peut authentifier une identité numérique, mais ne devient pas automatiquement la source de vérité des utilisateurs, groupes, ACL ou permissions Pixs.

Le backend Django reste l'autorité pour les règles métier, les transactions et l'autorisation. PostgreSQL reste la source de vérité applicative.

Le provider ne peut établir qu'un niveau d'assurance couvert par sa configuration de confiance. L'identifiant externe canonique est le triplet `(provider_id, issuer, subject)` ; une adresse e-mail, un nom affiché ou une claim non vérifiée ne constitue pas une clé de rapprochement. La liaison avec une identité existante est une opération explicite, vérifiée, idempotente et auditée.

## 4. Articulation avec OpenSpec et choix techniques ouverts

Les spécifications OpenSpec actives définissent les exigences normatives applicables aux domaines ci-dessous. La présente liste ne les duplique pas : elle recense les choix techniques concrets qui restent volontairement ouverts pour l'implémentation ou qui devront être précisés par une évolution OpenSpec si leur décision modifie un comportement normatif :

* les identifiants internes stables des utilisateurs et identités numériques ;
* les contraintes d'unicité du lien utilisateur-identité ;
* la représentation des comptes de service ;
* les sessions, tokens et méthodes d'authentification ;
* le modèle d'`AuthenticationContext`, des preuves et des niveaux d'assurance ;
* la révocation immédiate ou différée ;
* le step-up, la fraîcheur maximale et les exigences d'assurance par action ;
* le provisionnement et le déprovisionnement fédérés ;
* le mapping des identifiants externes ;
* la confiance des issuers, audiences, algorithmes, clés et claims des providers ;
* l'audit des authentifications et changements d'état ;
* la liaison explicite de comptes et la récupération sans élévation implicite ;
* les règles d'autorisation applicables aux identités sans utilisateur ;
* le schéma des politiques, selectors, conditions, obligations et versions ;
* les contrats `authorize` et `filter_authorized` ainsi que les décisions groupées ;
* les règles de priorité `DENY`/`ALLOW`, de cohérence, de cache et d'invalidation ;
* la résolution bornée des groupes imbriqués et la traçabilité acteur/délégation ;
* les règles de migration depuis une éventuelle représentation utilisateur historique.
* les états métier, de persistance, de rétention et de projection des données ;
* le schéma des politiques de cycle de vie, de suppression logique, de purge, de restauration et de legal hold ;
* les tombstones, le journal d'effacement et leur propagation aux caches, index, projections et synchronisations ;
* les garanties de cascade inter-modules, d'historique, de concurrence et de sauvegarde ;
* le schéma versionné du `DataGovernanceProfile`, les propriétaires techniques et les sources de vérité ;
* la taxonomie de confidentialité, de données personnelles et de secrets, ainsi que le comportement des données non classifiées ;
* les finalités, la lignée, les consommateurs, processeurs, contraintes de résidence ou de transfert et politiques d'export ;
* le contrat générique de `DataSubjectRequest`, son autorisation, son traitement asynchrone, son audit et sa propagation aux dérivés ;
* les obligations de confidentialité applicables aux APIs, événements, webhooks, observabilité, recherches, caches, fichiers, sauvegardes et exports ;
* le descripteur de capacité, le registre de résolution et les états distincts de disponibilité ;
* le schéma des feature flags, des affectations et des décisions d'évaluation ;
* les dimensions de ciblage, la cohorte déterministe, la priorité, le repli, l'expiration et l'invalidation des flags ;
* les règles d'application des flags aux APIs, événements, Jobs, frontend, permissions, données, migrations et providers ;
* le contrat versionné de `BulkOperation`, ses états, ses variantes `IMPORT` et `EXPORT` et son rattachement aux `operation_id` et Jobs persistants ;
* les formats de référence, les mappings versionnés, le staging privé, les checksums, les modes de commit et les stratégies de conflit des imports ;
* les projections autorisées, les snapshots ou watermarks, les manifestes, la rétention et les références temporaires des exports ;
* les quotas, seuils d'asynchronisme, checkpoints, annulation, retries, dead-letter, audit et propagation du tenant, du scope et de la gouvernance ;
* le périmètre des SDK TypeScript et Python, leurs transports, façades, mécanismes d'authentification et support des opérations synchrones, asynchrones et bulk ;
* la génération déterministe depuis OpenAPI, les contrats événementiels compatibles avec AsyncAPI et JSON Schema, la séparation entre code généré et façades maintenues et la matrice de compatibilité des SDK ;
* le Developer Kit, la CLI, le scaffolding, les validateurs de manifests et les suites de conformité pour les Components, modules, providers et extensions ;
* les règles de propagation du tenant, du scope, de la corrélation, de l'idempotence, des erreurs et des limites dans les clients SDK ;
* la gestion injectable des credentials, l'absence de persistance locale des tokens navigateur, la vérification des webhooks et les canaux de distribution des packages ;
* le modèle des entitlements, de leur contexte, de leurs décisions, de leurs états, de leurs portées, de leurs expirations et de leurs révocations ;
* le modèle des politiques de quota, buckets, unités, périodes, agrégations, consommations et réservations ;
* les contrats `EntitlementProvider` et `QuotaProvider`, la source de vérité, les garanties atomiques, la cohérence des caches et le comportement en indisponibilité ;
* l'ordre de résolution entre capacité, entitlement, autorisation, feature flag et quota, ainsi que les réponses d'erreur et diagnostics associés ;
* les règles de réservation, réconciliation et libération pour les APIs, Jobs, Commands asynchrones, imports, exports et opérations bulk ;
* la rétention, la confidentialité, l'agrégation et l'audit des décisions et données de consommation, sans introduire de facturation dans le Kernel ;
* le contrat `OfflineSyncCapability`, les ressources et Commands éligibles, les états locaux et les limites de fraîcheur ;
* les modèles `LocalReplica`, `OfflineCommand` et, lorsque nécessaire, `OfflineAccessLease`, leurs versions, checkpoints, idempotence et rétention ;
* le provider de stockage local, l'isolation appareil/utilisateur/tenant/scope, le chiffrement, l'effacement et l'absence de secrets ou tokens locaux ;
* le protocole de reconnexion, de réévaluation serveur, de réconciliation avec PostgreSQL, l'outbox et les Jobs, ainsi que les stratégies de conflit et de révocation ;
* les règles de compatibilité des schémas locaux et protocoles de synchronisation entre releases, sans imposer Electric, une base navigateur ou un service worker ;
* le contrat `TenantPlacementPolicy`, le `ResidencyContext`, les régions logiques, les versions, les epochs et les états de placement ;
* les règles d'héritage entre tenant, scopes enfants, ressources et classes de données, ainsi que la séparation des ressources platform-scoped ;
* les contrats de placement, réplication, chiffrement, clés, sauvegarde, restauration, suppression et révocation des providers régionaux ;
* le routage après résolution de l'identité, du tenant et du scope, les transferts inter-régions et les erreurs de région ou de résidence ;
* les garanties de primaire unique, fencing, bascule active-passive, split-brain, cohérence, quotas et idempotence entre régions ;
* les migrations de tenant, restaurations inter-régions et changements de politique, y compris les logs, traces, caches, index, événements, webhooks et copies offline ;
* les conditions d'une éventuelle topologie active-active ou multi-primary, qui ne fait pas partie de la référence du Kernel ;

Ces exigences ne doivent pas introduire de relation plusieurs-à-plusieurs entre utilisateurs et identités numériques sans décision architecturale explicite.

### 4.1 Modèle d'assurance d'authentification

Une authentification réussie produit un `AuthenticationContext` vérifié et limité dans le temps. Il est distinct de la `DigitalIdentity`, de la session et du credential utilisés pour l'établir.

```text
AuthenticationContext
├── digital_identity_id
├── provider_id
├── issuer
├── external_subject
├── authentication_time
├── expires_at
├── authentication_methods
├── identity_assurance
├── authentication_assurance
├── federation_trust
├── session_id éventuel
├── credential_id éventuel
└── ScopeContext
```

Les trois dimensions d'assurance sont évaluées séparément :

```text
identity_assurance       CLAIMED | VERIFIED | PROOFED
authentication_assurance SINGLE_FACTOR | MULTI_FACTOR | PHISHING_RESISTANT
federation_trust         UNTRUSTED | TRUSTED | STRONGLY_BOUND
```

Ces niveaux sont des sémantiques internes. Un provider doit déclarer le mapping de ses méthodes, claims, preuves et contextes vers ces niveaux, ainsi que le niveau maximal qu'il est autorisé à produire. `amr`, `acr`, le contexte SAML, la possession d'une clé ou une attestation ne sont jamais interprétés sans cette politique.

Le contexte est immuable pendant une opération et associé au `ScopeContext` résolu. Une autorisation sensible doit vérifier l'identité, l'expiration, la fraîcheur, la révocation, le niveau d'assurance requis et le périmètre de scope avant d'exécuter la Command. Si le niveau est insuffisant, le backend refuse l'opération ou déclenche un step-up explicite ; le frontend ne peut pas simuler cette élévation.

### 4.2 Confiance des providers et identifiants externes

La confiance d'un provider est configurée explicitement par installation, plateforme ou tenant selon le besoin. Elle doit au minimum contrôler `provider_id`, `issuer`, `audience`, algorithmes acceptés, clés de signature, fenêtre temporelle, mapping des identifiants, claims obligatoires, niveau d'assurance maximal et conditions de révocation. La découverte, la présence dans un package ou la seule validité cryptographique d'un token ne suffit pas à établir la confiance applicative.

L'identifiant externe canonique est le triplet `(provider_id, issuer, subject)`. Le mapping vers une `DigitalIdentity` est déterministe et auditable. Une adresse e-mail, un nom affiché ou une claim non vérifiée ne constitue pas une clé de rapprochement. Une liaison de comptes exige la preuve des deux côtés, une confirmation explicite, une vérification d'unicité et un audit.

### 4.3 Sessions, facteurs et récupération

Une session représente une période d'accès et conserve une référence vers le contexte d'authentification, son expiration, son état, sa dernière authentification, sa fraîcheur et son périmètre. Le contrat accepte une session opaque côté serveur ou un artefact autonome validé par le backend, sans imposer une topologie de session aux providers.

Les tokens d'accès sont bornés par la politique du provider. Les mécanismes de renouvellement doivent supporter la rotation, la détection de réutilisation et la révocation. Une révocation d'identité, de credential, de session, de provider ou de politique de confiance doit invalider les contextes concernés sans supprimer l'identité de référence ni les données métier. Les événements de révocation, expiration, verrouillage, step-up, liaison et récupération sont auditables et ne journalisent jamais les secrets.

Le framework ne rend pas un mot de passe obligatoire. Un provider local peut fournir des credentials, tandis que des providers OIDC, SAML, WebAuthn, mTLS, device ou workload identity peuvent fournir d'autres méthodes. Les identités `SERVICE` et `DEVICE` déclarent une méthode adaptée, une durée de validité, des limites de périmètre et des règles de rotation. Une API key seule produit au plus une assurance de base, sauf politique explicite contraire.

La récupération révoque les sessions concernées, remplace ou invalide le credential compromis et ne restaure pas automatiquement `VERIFIED`, `PROOFED`, `MULTI_FACTOR` ou `PHISHING_RESISTANT` sans nouvelle preuve ou intervention administrative autorisée.

## 5. Modèle commun de composant

Tout élément extensible de Pixs utilise conceptuellement le modèle commun `Component`.

Les types de composants sont :

```text
KERNEL
MODULE
SUBMODULE
PROVIDER
EXTENSION
THEME
```

Les contrats, capacités et services ne sont pas des types de composants. Un composant peut fournir une capacité, implémenter un contrat ou enregistrer un service.

Chaque composant doit disposer d'un identifiant canonique stable, d'un type, d'une version, d'un manifest, de dépendances déclarées et d'un état de lifecycle inspectable.

`Component` décrit une frontière de composition et de gouvernance, pas une entité métier. Le modèle commun est appliqué aux modules, sous-modules, providers, extensions et thèmes sans imposer à ces composants une persistance, une structure de données ou une implémentation d'exécution identique. Les propriétés communes concernent uniquement l'identification, la composition, les contrats, les capacités, la configuration, la sécurité, le lifecycle et le diagnostic.

## 6. Identifiants et manifests

Le manifest de chaque composant est un fichier TOML nommé `component.toml`.

Les identifiants officiels utilisent le namespace réservé `pixs.*`. Les composants externes utilisent un namespace fournisseur.

```text
pixs.core
pixs.authentication.oidc
acme.crm
acme.storage.s3
```

L'identifiant canonique est indépendant du chemin physique, du nom de paquet, de l'ordre de découverte et de l'implémentation Python. Un renommage d'identifiant constitue une évolution incompatible.

Le manifest doit pouvoir décrire au minimum :

* l'identifiant canonique ;
* le type de composant ;
* la version SemVer ;
* les dépendances obligatoires et optionnelles ;
* les capacités requises et fournies ;
* les contrats implémentés ;
* les services enregistrés ;
* la configuration et son schéma ;
* la compatibilité déclarée ;
* les contributions publiques du composant.

Lorsqu'ils sont pertinents, le manifest doit également référencer le propriétaire des données, les migrations, le profil de sécurité, les permissions techniques, les frontières réseau, les points d'entrée autorisés, les contributions frontend et les définitions de capacités ou de feature flags fournies par le composant. Le manifest est déclaratif, non exécutable et unique par composant. Il ne peut contenir ni secret, ni logique métier, ni expression à évaluer.

Les points d'entrée sont résolus uniquement après validation du manifest et doivent rester dans le périmètre déclaré du composant. Une simple présence sur le filesystem, une importabilité Python ou une dépendance transitive ne suffit pas à enregistrer un composant ou une contribution.

Exemple conceptuel :

```toml
schema_version = "1"
id = "pixs.authentication.oidc"
type = "PROVIDER"
version = "1.0.0"

[dependencies]
components = ["pixs.core >=1.0.0 <2.0.0"]
capabilities = ["authentication >=1.0.0 <2.0.0"]

[optional_dependencies]
capabilities = ["audit"]

[provides]
capabilities = ["authentication.oidc"]

[implements]
contracts = ["pixs.authentication.contract"]
```

## 7. Dépendances et résolution

Une dépendance obligatoire absente, incompatible ou cyclique invalide la composition. Une dépendance optionnelle absente n'invalide pas la composition, mais le composant doit déclarer un comportement cohérent sans cette capacité.

La résolution d'un provider suit exclusivement cette règle :

```text
provider explicitement configuré
        ↓ sinon
provider compatible unique
        ↓ sinon
composition invalide
```

La sélection ne doit jamais dépendre de l'ordre du filesystem, des imports ou de l'installation. Plusieurs providers pour une même capacité nécessitent une composition explicite, par exemple un provider composite ou un routeur déclaré.

Les composants, contrats et capacités publiques utilisent SemVer 2.0.0. Les contraintes de compatibilité sont vérifiées avant activation. Les versions de composant, de contrat, de capacité et de schéma de manifest sont conceptuellement distinctes.

### 7.1 Descripteur et disponibilité d'une capacité

Les capacités fournies et requises sont résolues au niveau de la composition, avant l'activation du composant qui les consomme. Le registre de capacités ne dépend ni du chemin physique, ni de l'ordre de découverte, ni d'un flag runtime.

```text
CapabilityDescriptor
├── capability_id
├── capability_version
├── owner_component
├── contract_refs
├── provider_ref éventuel
├── requiredness       REQUIRED | OPTIONAL
├── configuration_ref éventuelle
└── fallback_policy éventuelle
```

La disponibilité d'une capacité est une dimension distincte du lifecycle du composant :

```text
DECLARED → RESOLVED → AVAILABLE
                         ├── DEGRADED
                         ├── DISABLED
                         └── BLOCKED
```

`RESOLVED` signifie que le contrat, le provider et les dépendances sont déterminés ; `AVAILABLE` signifie que la capacité peut être utilisée ; `DEGRADED`, `DISABLED` et `BLOCKED` exposent respectivement une garantie réduite, une désactivation explicite ou une impossibilité bloquante. Une capacité obligatoire qui n'est pas `AVAILABLE` empêche l'activation ou le passage à `ready`. Une capacité optionnelle doit déclarer le comportement attendu dans les autres états.

### 7.2 Feature flags runtime

Un feature flag est une politique de sélection d'un comportement déjà présent dans l'artefact et compatible avec les contrats déclarés. Il ne constitue ni une permission, ni une dépendance, ni un mécanisme de migration, ni une sélection implicite de provider.

```text
FeatureFlagDefinition
├── flag_id
├── flag_version
├── owner_component
├── purpose
├── value_schema       BOOLEAN | VARIANT
├── default_value
├── targeting_dimensions
├── cohort_key éventuelle
├── prerequisites
├── fallback_policy
├── expires_at
└── audit_policy
```

Les affectations runtime sont séparées de la définition :

```text
FeatureFlagAssignment
├── flag_id
├── selector             INSTALLATION | ENVIRONMENT | TENANT | SCOPE
├── selector_value
├── value ou variant
├── valid_from / valid_until
├── configuration_version
└── updated_by
```

Le contexte d'évaluation comprend uniquement les dimensions déclarées par le flag. Le socle P2 prend en charge l'installation ou l'environnement, le tenant et le scope enfant ; le ciblage individuel et l'expérimentation statistique ne sont pas des primitives natives. La priorité d'une affectation est déterministe, du périmètre général vers le périmètre le plus spécifique, et aucune relation de scope ou de tenant n'est élargie implicitement.

Un déploiement progressif utilise une `cohort_key` déclarée et un calcul stable. Il ne doit pas tirer un résultat aléatoire à chaque requête. Les règles sont déclaratives, bornées et sans expression ou code arbitraire à exécuter.

La source de vérité des affectations est persistante et versionnée. Les processus peuvent conserver un cache local borné, mais doivent vérifier sa durée de validité et son numéro de configuration ; une invalidation ou une mise à jour ne peut pas être masquée par un cache périmé. Les changements de flags sont des opérations administratives authentifiées, autorisées, corrélées et auditables, sans être embarqués dans un paquet Debian, une image Docker ou un bundle frontend.

Une valeur absente, invalide ou périmée applique la politique de repli déclarée. L'échec est fermé pour une permission, une mutation, une donnée protégée ou un contrat ; un repli différent n'est autorisé que pour une fonctionnalité non sensible. Le frontend peut adapter son affichage, mais le backend réévalue toujours le flag avant toute mutation ou exposition protégée.

Les Commands évaluent le flag au point où le comportement est exécuté. Un Job ou un handler d'événement réévalue la configuration au moment de son exécution ; lorsqu'une opération exige de conserver la sémantique choisie à sa création, sa version de flag et sa valeur sont persistées dans son contrat d'opération. Une évolution de schéma ou de contrat doit rester compatible indépendamment de l'état du flag.

Le lifecycle d'un flag est distinct du lifecycle d'un composant :

```text
DRAFT → ACTIVE → PAUSED → EXPIRED → RETIRED
```

L'expiration bloque les nouvelles affectations et produit un diagnostic ; elle ne supprime pas implicitement le code, les données ou les contrats. La retraite d'un flag exige une décision de nettoyage ou de migration explicitement validée.

## 8. Contrats publics

Les contrats publics sont des interfaces stables entre composants Pixs. Ils sont enregistrés séparément des composants qui les implémentent.

Les catégories de contrats sont :

```text
SERVICE  opération synchrone fournie par un composant
COMMAND  demande explicite de mutation
QUERY    demande explicite de lecture
EVENT    fait déjà survenu
HOOK     point d'extension déclaré
SCHEMA   structure de données ou de configuration contractuelle
API      interface de consommation externe ou inter-composants
```

Chaque contrat public doit disposer d'un identifiant canonique stable, d'une catégorie, d'une version, d'un composant propriétaire et de garanties documentées. L'implémentation privée d'un composant ne constitue pas un contrat public par défaut.

Les catégories ne sont pas interchangeables : un `EVENT` ne remplace pas un `COMMAND`, un `HOOK` ne constitue pas une garantie transactionnelle et un `SCHEMA` ne définit pas à lui seul une règle d'autorisation.

### 8.1 Contrat d'extension

Une extension est une contribution à un point d'extension public d'un composant cible. Le point d'extension possède un identifiant namespacé, une catégorie, une version, un schéma de contribution, un propriétaire et des garanties documentées. Les catégories d'extension peuvent notamment être `SERVICE`, `COMMAND`, `QUERY`, `EVENT`, `HOOK`, `ROUTE`, `NAVIGATION`, `UI_SLOT`, `VALIDATION` ou `CONFIGURATION`.

Une contribution doit déclarer au minimum son identifiant stable, son composant cible, le point d'extension utilisé, la version du contrat, son point d'entrée, ses dépendances, ses permissions, son niveau de confiance et ses conditions d'activation. Les collisions sont refusées par défaut ; lorsqu'une composition autorise plusieurs contributions, sa politique de fusion, de priorité et d'ordre doit être explicitement déclarée et déterministe.

Une extension ne peut pas importer une implémentation privée, modifier directement les données d'un autre composant ou transformer un événement, un hook ou une contribution d'interface en autorisation métier. Les mutations sensibles restent des Commands évaluées par Django.

Les extensions backend chargées dans le processus sont considérées comme du code de confiance après validation de l'artefact et de la composition. Les extensions frontend de référence sont composées au build et utilisent les APIs publiques du shell. Le chargement distant, l'installation runtime et l'évaluation dynamique de code sont interdits par défaut. Une extension non pleinement fiable doit utiliser un adapter d'isolation, tel qu'un sandbox ou un iframe, avec une API explicitement limitée.

## 9. Versionnement des contrats

Les contrats publics utilisent SemVer 2.0.0 indépendamment de la version du composant qui les implémente.

```text
release_version
component_version
contract_version
capability_version
manifest_schema_version
schema_version
migration_version
event_version
api_version
configuration_schema_version
data_governance_version
feature_flag_version
bulk_operation_version
sdk_version
entitlement_version
quota_policy_version
offline_capability_version
local_schema_version
sync_protocol_version
residency_policy_version
placement_policy_version
region_topology_version
```

Ces versions peuvent évoluer séparément. Une correction interne compatible peut modifier la version du composant sans modifier la version du contrat. Une release est corrélée à une composition précise de ces versions, mais ne les remplace pas.

Une évolution est considérée comme majeure lorsqu'elle modifie de manière incompatible, notamment :

* l'identifiant ou la catégorie du contrat ;
* les entrées ou sorties obligatoires ;
* les garanties d'erreur ou de transaction ;
* les règles de livraison ou d'ordre des événements ;
* la sémantique observable par le consommateur.

Une évolution rétrocompatible peut ajouter un élément optionnel ou corriger un comportement sans modifier les garanties publiques. Elle relève alors d'une version mineure ou corrective selon son impact.

## 10. Compatibilité et dépréciation

Un composant consommateur doit déclarer les contraintes de version des contrats dont il dépend. Le Kernel doit vérifier ces contraintes avant activation et lors d'une mise à niveau.

```text
contract = "pixs.authentication.contract >=1.0.0 <2.0.0"
```

Une incompatibilité connue doit produire un échec explicite. Pixs ne doit pas supposer qu'une implémentation est compatible uniquement parce qu'elle porte un nom proche ou une version plus récente.

Une dépréciation doit être annoncée dans une version mineure, documenter son remplacement éventuel et conserver le contrat compatible pendant toute la version majeure courante. Sa suppression n'est autorisée qu'à partir de la version majeure suivante, sauf exception de sécurité critique, obligation légale ou impossibilité technique majeure explicitement justifiée.

Un contrat peut prolonger volontairement sa période de dépréciation. La durée n'est pas exprimée en mois afin de rester indépendante du rythme de publication des applications.

Les composants implémentant un contrat peuvent être soumis à une suite de tests de conformité commune. La compatibilité déclarative et la conformité comportementale sont complémentaires et ne doivent pas être confondues.

La compatibilité globale est représentée par une matrice calculée avant activation ou mise à niveau :

```text
CompatibilityMatrix
├── release / runtime
├── composants et capacités
├── contrats et APIs
├── schémas et migrations de données
├── événements
├── providers
├── configuration
└── clients frontend

état : COMPATIBLE | REQUIRES_MIGRATION | DEPRECATED | BLOCKED
```

Une version plus récente n'est compatible que si ses garanties sont démontrées pour le consommateur concerné. La release courante doit être compatible avec la release immédiatement précédente ; un chemin depuis une release plus ancienne passe par les migrations intermédiaires déclarées. Un saut de version non déclaré, une dépendance non résolue ou une période de coexistence non démontrée bloque l'activation.

### 10.1 Contrat et exécution des migrations

Les migrations sont définies et possédées par le module qui possède les données. Une migration expose conceptuellement :

```text
migration_id
module_id
version_source
version_cible
dependencies
preconditions
postconditions
idempotent
destructive
execution_mode      ONLINE | MAINTENANCE | OFFLINE
compensation_policy
```

Les migrations d'un module forment une chaîne versionnée. Le planificateur global résout les dépendances entre modules dans un graphe déterministe, sans écriture directe dans les données privées d'un autre module. Un saut n'est accepté que si une migration de compatibilité explicite le permet.

Le plan de mise à niveau suit, lorsque nécessaire, les phases suivantes :

```text
PRECHECK
    ↓
EXPAND
    ↓
MIGRATE / BACKFILL reprenable
    ↓
SWITCH compatible
    ↓
fenêtre de coexistence N / N+1
    ↓
CONTRACT différée et destructive
```

Les opérations de backfill doivent être reprenables, idempotentes, bornées et observables. Une étape destructive ne peut être exécutée qu'après vérification des consommateurs actifs, de la période de dépréciation et des sauvegardes ou procédures de restauration applicables.

L'exécution est déclenchée par une commande d'exploitation autorisée et conserve un état persistant, au minimum `PLANNED`, `PRECHECKED`, `RUNNING`, `PAUSED`, `SUCCEEDED`, `FAILED` ou `BLOCKED`. Un échec ne doit pas laisser croire que la composition est activée. Le démarrage peut effectuer le `PRECHECK`, mais ne doit pas exécuter une migration en attente ni déclarer `ready` une instance dont la migration bloquante n'est pas terminée.

Les migrations de schéma sont forward-only par défaut. Un rollback applicatif n'est autorisé que si la matrice de compatibilité prouve que le code précédent accepte le schéma et les données actuels ; sinon, Pixs applique une correction vers l'avant ou une restauration vérifiée. Aucun downgrade automatique de la base ne doit être lancé pour masquer un échec de release.

## 11. Multi-tenancy

`Tenant` est la frontière technique d'isolation des données et du contexte d'autorisation. `Organization` peut représenter une entité métier, mais ne constitue pas nécessairement une frontière technique.

Le modèle commun expose un type logique `Scope` et un `ScopeContext`. `Tenant` est le scope racine obligatoire ; un scope enfant possède un parent unique, appartient au même tenant et ne peut former de cycle. Les types `Organization`, `Workspace`, `Project` ou équivalents sont des types namespacés fournis par les modules qui en possèdent le modèle métier. Le Core ne doit pas transformer un type métier en frontière d'isolation sans déclaration explicite.

Une ressource a une propriété canonique unique. Pour une ressource tenant-scoped, `tenant_id` identifie le tenant racine et `scope_id`, lorsqu'il est renseigné, identifie le scope enfant propriétaire. `scope_id` ne peut jamais référencer un scope d'un autre tenant. Une ressource platform-scoped est explicitement hors tenant et hors scope ; elle ne doit pas être rendue accessible dans un contexte tenant par défaut. Le partage, la délégation et l'héritage entre scopes passent par des ACL, rôles ou relations déclarés et ne changent pas la propriété canonique.

Le modèle doit supporter :

```text
DigitalIdentity N ─── N Tenant
          via TenantMembership
```

Une appartenance doit être explicitement représentée, activable, révocable et contextualisée. Une identité numérique peut appartenir à plusieurs tenants. Les comptes de service suivent le même modèle d'appartenance, sans nécessiter d'utilisateur humain.

Pixs doit supporter le mode mono-tenant et le mode multi-tenant. Le mode mono-tenant ne supprime pas les invariants tenant-scoped ; il utilise un tenant courant unique ou un contexte équivalent explicitement configuré.

Les groupes sont tenant-scoped par défaut. Les groupes globaux sont réservés aux besoins de plateforme et leur utilisation dans un tenant doit être explicitement déclarée.

L'implémentation de référence initiale utilise une base PostgreSQL partagée avec un schéma commun et des références explicites `tenant_id`/`scope_id`. Django applique les contrôles d'isolation et d'autorisation ; la Row-Level Security PostgreSQL peut fournir une défense en profondeur lorsque le provider et la topologie la supportent. Une évolution vers un schéma par tenant, une base par tenant ou une isolation régionale doit conserver les mêmes contrats fonctionnels et ne peut pas être codée dans les modules métiers.

## 12. Autorisation et contexte

L'évaluation d'une autorisation utilise les éléments suivants :

```text
Subject  → identité numérique, utilisateur ou groupe
Resource → ressource protégée
Action   → opération demandée
    Context  → ScopeContext courant et autres contraintes applicables
```

Les rôles regroupent des permissions. Les ACL permettent des règles fines sur une ressource ou un périmètre. Les modules déclarent leurs ressources et actions sans déplacer la logique métier dans le Kernel.

L'algorithme de décision est :

```text
DENY explicite
      ↓ sinon
ALLOW explicite
      ↓ sinon
deny by default
```

Toute ressource tenant-scoped doit être évaluée avec un `ScopeContext` valide : `tenant_id` est obligatoire et `scope_id` est fourni lorsque le contrat de la ressource le requiert. Le contexte est résolu avant l'autorisation, immuable pendant l'opération et propagé aux Commands, Queries, Events, Jobs, projections, caches, fichiers, recherches, workflows, synchronisations et audits. Les accès plateforme et inter-tenants nécessitent une permission explicite, un contexte d'accès explicite et un événement d'audit. Ils ne constituent jamais un bypass silencieux des ACL. Un accès à un scope parent ou descendant n'est pas implicite.

Le backend Django est l'autorité d'évaluation. Le frontend, les caches, les projections et Electric peuvent refléter une décision mais ne peuvent pas l'autoriser à la place du backend.

### 12.1 Modèle de politique

Le moteur de référence de `pixs.core` est un PDP déclaratif. Django joue le rôle de PEP à la frontière des API, Commands, Queries, Jobs, fichiers, recherches et opérations d'exploitation. Une interface d'administration des politiques joue le rôle de PAP ; ses propres opérations sont soumises à l'autorisation, au step-up lorsque requis et à l'audit. Un PDP externe peut être utilisé comme adapter, mais il doit respecter le même contrat de décision et ne peut pas devenir obligatoire pour le Kernel.

Une politique doit pouvoir exprimer au minimum :

```text
policy_id
policy_version
owner_component
effect                 DENY | ALLOW
subject_selector
resource_selector
action_selector
scope_selector
conditions typées
obligations éventuelles
valid_from / valid_until éventuels
```

Les selectors, conditions et obligations sont déclaratifs, versionnés, bornés et validables. Ils ne doivent ni exécuter de code arbitraire, ni charger une expression distante, ni accéder directement à une table privée d'un module. Les modules restent propriétaires de leurs ressources, actions, relations et politiques fonctionnelles.

L'évaluation suit strictement `DENY explicite`, puis `ALLOW explicite`, puis `deny by default`. Un `DENY` correspondant à un sujet, une ressource, une action et un périmètre valide prévaut sur tout `ALLOW`. La propriété d'une ressource, l'appartenance à un groupe, un rôle administrateur ou la présence dans un scope parent ne sont que des attributs ou relations évaluables ; ils ne créent pas d'autorisation implicite.

### 12.2 Contrat de décision et filtrage

Le contrat `authorize` retourne conceptuellement :

```text
decision_id
effect                   ALLOW | DENY
reason_code
policy_version
obligations éventuelles
evaluated_at
expires_at éventuel
```

Le motif détaillé et la trace d'évaluation sont réservés aux diagnostics autorisés. La frontière publique expose une erreur stable et minimale, sans révéler les politiques privées, les attributs sensibles ou les raisons exploitables d'un refus.

Le contrat `filter_authorized` traduit la même décision en contrainte appliquée à la source de données avant pagination, projection, recherche ou export. Il est obligatoire pour les collections et ne peut pas être remplacé par un filtrage frontend. Une opération groupée doit pouvoir retourner des décisions par ressource ou échouer en bloc selon le contrat de la capacité.

### 12.3 Cohérence, cache et invalidation

Une mutation et toute action sensible réévaluent la politique courante, l'`AuthenticationContext`, le `ScopeContext`, la révocation et la fraîcheur requise. Une décision `ALLOW` périmée ne doit jamais autoriser l'opération. Les caches de lecture, lorsqu'ils sont permis, sont indexés par sujet, ressource, action, tenant, scope, assurance et version ou epoch de politique ; ils sont invalidés après modification d'une politique, ACL, rôle, membership, scope, révocation ou assurance.

Une indisponibilité du PDP produit un refus fermé pour les mutations, les actions sensibles et les données protégées. Un mode dégradé pour des lectures publiques ou explicitement non sensibles doit être déclaré par la capacité et ne peut pas être généralisé par le runtime.

### 12.4 Groupes, délégation et élévation

La résolution des groupes imbriqués doit utiliser un graphe acyclique, borné et détectable avant activation. Un cycle, une profondeur excessive ou une relation ambiguë produit un refus ou une composition invalide selon le moment de détection.

Le contexte de décision peut distinguer l'acteur effectif, le sujet représenté et l'éventuel délégant afin de préserver la traçabilité. Une délégation, une impersonation ou une élévation break-glass doit être explicitement accordée, limitée dans le temps, liée à un périmètre, soumise au niveau d'assurance requis et auditée. Aucun rôle permanent de contournement ne doit être créé par défaut.

## 13. Identifiants des données

Les entités persistées par Pixs utilisent UUIDv7 comme identifiants internes.

```text
entity_id    → UUIDv7
component_id → identifiant textuel namespacé
contract_id  → identifiant textuel namespacé
external_id  → identifiant fourni par un provider, séparé
```

Les UUIDv7 sont générés indépendamment d'un compteur local de base de données. Ils sont stables, globalement uniques et adaptés aux références inter-modules et aux index persistants.

Un identifiant externe OIDC, SAML, LDAP ou autre ne doit jamais être utilisé implicitement comme identifiant interne Pixs. Le mapping entre identifiant externe et entité Pixs doit être explicite, unique selon le provider et auditable.

Les identifiants de composants et de contrats restent des chaînes namespacées, par exemple `pixs.core` ou `pixs.authentication.contract`. Un renommage d'identifiant constitue une évolution incompatible et doit être traité comme telle.

## 14. Champs communs et cycle de vie des données

Une entité persistée doit utiliser, lorsque ces informations sont pertinentes :

```text
id          UUIDv7 interne et stable
created_at  horodatage UTC immuable
updated_at  horodatage UTC modifiable
version     compteur de concurrence optimiste
    tenant_id   UUIDv7 du tenant racine si la ressource est tenant-scoped
    scope_id    UUIDv7 du scope enfant propriétaire lorsque la ressource n'est pas portée directement par le tenant
```

Les horodatages doivent être générés et interprétés en UTC. Le champ `version` permet de détecter les mises à jour concurrentes sans faire de la dernière écriture une résolution implicite.

Le `soft delete` n'est pas une obligation globale du framework. Le module propriétaire doit déclarer la stratégie applicable : suppression physique, marqueur de suppression, archivage ou conservation définitive. Toute suppression doit respecter les références inter-modules, les obligations d'audit et les règles de rétention.

Une entité tenant-scoped doit posséder une référence explicite vers son tenant racine. Lorsqu'elle est rattachée à un scope enfant, elle doit conserver un `scope_id` cohérent avec ce tenant. Une entité platform-scoped doit être déclarée comme telle et ne doit pas recevoir de scope par défaut. Le contexte tenant ou scope d'une requête ne doit pas être déduit uniquement d'un identifiant fourni par le client.

### 14.1 Dimensions du cycle de vie

Le cycle de vie d'une donnée comporte plusieurs dimensions qui ne doivent pas être confondues :

```text
état métier       défini par le module propriétaire
persistance       ACTIVE | ARCHIVED | SOFT_DELETED | PURGE_PENDING
rétention         RETAINED | LEGAL_HOLD | ELIGIBLE_FOR_PURGE
projection        état dérivé, reconstruisible ou synchronisé
```

Le module reste propriétaire de l'état métier, de ses invariants et de la politique déclarée. Pixs fournit les mécanismes communs de marquage, filtrage, rétention, tombstone, purge, restauration, historique et propagation. `PURGED` n'est pas nécessairement conservé comme une ligne métier : un tombstone ou un journal d'effacement durable doit toutefois être conservé lorsque cela est requis pour empêcher une résurrection ou démontrer l'effacement.

Une politique de cycle de vie expose conceptuellement :

```text
retention_period
deletion_strategy       SOFT_DELETE | PHYSICAL_DELETE | ARCHIVE | IMMUTABLE
restore_allowed
purge_conditions
legal_hold_supported
cascade_policy          RESTRICT par défaut
history_policy
```

Le schéma exact est défini par la capacité concernée et peut ajouter une politique de synchronisation ou de classification. Une ressource métier utilise `SOFT_DELETE` par défaut. Les requêtes normales excluent les états `SOFT_DELETED` et `PURGE_PENDING` ; une restauration est une Command explicite, autorisée, auditée et soumise à la version de concurrence. Les données éphémères ou soumises à une obligation d'effacement immédiat doivent déclarer leurs garanties spécifiques.

### 14.2 Suppression, rétention et purge

La suppression logique met à jour la ressource et ses métadonnées de cycle de vie dans une frontière transactionnelle. Les références nécessaires à l'audit, à la synchronisation et au tombstone ne doivent pas être supprimées prématurément. La décision de purge vérifie au minimum la fin de la rétention, l'absence de legal hold, les références bloquantes, la politique du module propriétaire et l'état des projections ou synchronisations concernées.

La purge physique est exécutée par un Job explicitement autorisé. Elle est idempotente, rejouable et observable ; une reprise ne doit ni réintroduire une donnée ni contourner une condition de rétention. Les suppressions inter-modules suivent `RESTRICT` par défaut. Une cascade doit être un contrat public ou une Command du module propriétaire, avec une politique, une corrélation et un audit propres ; une cascade SQL implicite entre propriétaires de modules est interdite.

### 14.3 Tombstones, projections et restauration

Un tombstone doit identifier sans payload sensible la ressource effacée, sa version de suppression, son instant, son tenant et son scope lorsque ces dimensions s'appliquent, ainsi que les informations nécessaires à la rétention, à la synchronisation et à la déduplication. Il est propagé par l'outbox ou le mécanisme de synchronisation déclaré vers les caches, index, projections, providers externes et consommateurs concernés. Une reconstruction doit consulter ces tombstones avant de republier une ressource.

Les sauvegardes ont une rétention indépendante de celle des données en ligne. Une restauration doit rejouer ou réconcilier le journal d'effacement et les tombstones applicables avant de rendre les données disponibles ; elle ne doit pas restaurer silencieusement une ressource supprimée. La purge physique d'une sauvegarde suit la politique de sauvegarde et les obligations de legal hold, sans faire de la sauvegarde une source de vérité applicative.

Les octets conservés par un `ObjectStorageProvider` suivent la décision portée par la métadonnée Pixs, mais peuvent avoir une durée de vie technique distincte. La suppression ou la purge doit donc coordonner la métadonnée, le tombstone et le provider, sans accès direct aux stockages privés d'un référentiel documentaire externe.

### 14.4 Concurrence et historique

Les mutations de cycle de vie utilisent `version` ou un mécanisme équivalent de concurrence optimiste lorsque la ressource est mutable. L'historique des transitions, décisions de rétention et purges est activé selon la `history_policy` et doit rester distinct des logs techniques. L'event sourcing est une capacité spécialisée optionnelle ; il n'est pas requis pour les ressources ordinaires et ne doit pas devenir une seconde source de vérité par défaut.

### 14.5 Gouvernance des données et confidentialité

Le cycle de vie décrit ce qui arrive à une donnée ; la gouvernance décrit ce qu'elle est, pourquoi elle est traitée, qui peut la recevoir et quelles obligations suivent ses copies. Chaque composant qui introduit, dérive ou transfère une donnée doit publier un profil de gouvernance versionné et possédé par le composant.

```text
DataGovernanceProfile
├── profile_version
├── data_asset_id
├── owner_component
├── source_of_truth
├── data_classes
├── confidentiality
├── personal_data
├── purpose_refs
├── retention_policy
├── deletion_policy
├── residency_constraints éventuelles
├── authorized_consumers
├── processor_refs éventuelles
├── export_policy
└── lineage
```

`source_of_truth` identifie le composant et le contrat autoritatifs ; `lineage` décrit les projections, index, caches, fichiers, sauvegardes, événements et synchronisations dérivés. Un dérivé ne devient pas une nouvelle source de vérité par copie. Le profil doit être attaché à la donnée ou à l'opération lorsque le format le permet et doit être conservé lors d'un changement de provider.

Les classifications sont orthogonales :

```text
confidentiality  PUBLIC | INTERNAL | CONFIDENTIAL | RESTRICTED
personal_data    NONE | PERSONAL | SENSITIVE_PERSONAL
secret           hors données métier, toujours référencé extérieurement
```

L'absence de classification n'est pas une permission implicite : elle applique la politique la plus restrictive. Une donnée non classifiée peut être persistée pour permettre une activation contrôlée, mais tout export, événement d'intégration, webhook, transfert à un provider ou exposition externe doit être refusé tant que la déclaration nécessaire n'est pas validée. Les classes métier et les finalités restent déclarées par le composant propriétaire ; Pixs ne leur impose pas de taxonomie de domaine.

La classification et les obligations associées doivent être prises en compte dans les APIs, événements, webhooks, logs, traces, audits, recherches, projections, caches, fichiers, sauvegardes et exports. Le moteur d'autorisation peut compléter sa décision par des obligations de masquage, de minimisation, d'interdiction d'export ou de rétention réduite ; ces obligations doivent être exécutées par le point d'application concerné et rester auditables.

Les providers externes ne sont pas propriétaires des données Pixs. Leur contrat doit déclarer, lorsque applicable, les garanties de transport, de chiffrement au repos, de localisation, de rétention, de suppression, de restitution, de versionnement et de révocation. Les clés et credentials sont fournis par références externes et ne figurent ni dans le profil, ni dans les manifests, ni dans les artefacts ou signaux techniques.

Les contraintes de résidence et de transfert sont optionnelles et déclaratives. Lorsqu'une contrainte existe, un flux sortant doit identifier son consommateur ou processeur, son but, sa classe de données, sa destination logique, ses garanties de transport et son mécanisme de suppression ou de révocation. Le contrat ne fixe ni région, ni fournisseur, ni topologie de déploiement ; la composition est refusée si une garantie déclarée n'est pas satisfaite.

### 14.6 Demandes relatives aux données

`DataSubjectRequest` est un contrat générique permettant à un module d'exposer, selon sa politique, les opérations `ACCESS`, `EXPORT`, `RECTIFY`, `ERASE` et `RESTRICT`.

```text
DataSubjectRequest
├── request_id
├── operation
├── subject_reference
├── tenant_id / scope_id éventuels
├── requested_by
├── status
├── policy_version
├── operation_id éventuel
├── legal_hold_decision éventuelle
└── result_reference éventuelle
```

La demande est une Command : elle vérifie l'identité, le `ScopeContext`, l'autorisation, la politique du module et la concurrence avant toute mutation. Elle peut être asynchrone et doit exposer un `operation_id` lorsque son traitement dépasse la requête. Son exécution est idempotente, auditée et ne modifie jamais directement les tables privées d'un autre module.

Le traitement doit coordonner la source de vérité, les projections, caches, index, fichiers, sauvegardes et providers déclarés. Il doit distinguer une restriction ou un effacement logique d'une purge physique, respecter la rétention et les legal holds et propager les tombstones ou décisions d'effacement sans exposer de payload sensible. Le framework ne déduit pas une obligation juridique ou un mécanisme de consentement à partir du seul nom de l'opération ; le module déclare les règles qui lui sont applicables.

### 14.7 Multi-région et résidence par tenant conditionnelles

La multi-région et la résidence sont des capacités optionnelles de gouvernance et d'exploitation. La référence Pixs reste mono-région : un tenant possède une région principale logique et aucune réplication, sauvegarde, transformation, bascule ou copie inter-région n'est activée implicitement. Les contraintes existantes de `DataGovernanceProfile` sont complétées par une politique de placement opérationnelle, sans imposer une région, un pays, une juridiction, un cloud ou une topologie au Kernel.

La résidence décrit les emplacements admissibles pour une classe de données et ses dérivés ; le placement décrit l'emplacement effectif du primaire, des réplicas, des traitements, des sauvegardes et des clés. Les identifiants de région sont logiques et leur correspondance avec un provider, une zone ou un emplacement physique est fournie par la configuration de déploiement validée.

Le contrat logique de placement est le suivant :

```text
TenantPlacementPolicy
├── tenant_id
├── placement_policy_version
├── home_region
├── allowed_replica_regions
├── allowed_processing_regions
├── allowed_backup_regions
├── allowed_key_regions
├── allowed_offline_copy_policy éventuelle
├── failover_mode        SINGLE_REGION | ACTIVE_PASSIVE
├── region_epoch
├── transfer_policy
├── status               ACTIVE | PENDING | MIGRATING | DEGRADED | BLOCKED
└── revision
```

La politique s'applique au tenant, à ses scopes enfants et aux ressources qui en dépendent. Un scope enfant ou un `DataGovernanceProfile` peut renforcer la contrainte, mais ne peut pas autoriser une région interdite par le tenant. Les ressources platform-scoped ont une politique séparée. Une ressource tenant-scoped possède une seule région d'autorité à un instant donné ; les réplicas distants, caches, index et projections restent non autoritatifs.

Le contexte régional est distinct du `ScopeContext` mais doit lui être corrélé :

```text
ResidencyContext
├── request_region éventuelle
├── tenant_home_region
├── data_region
├── residency_policy_version
├── placement_policy_version
├── region_epoch
├── data_class
├── transfer_allowed
└── processor_reference éventuelle
```

Le routage résout d'abord l'identité, le tenant et le scope, puis le `ResidencyContext` et le placement. Une région fournie par le client ne peut pas remplacer le contexte canonique. Les écritures sont dirigées vers la région primaire ; les lectures d'un replica indiquent leur fraîcheur et ne peuvent pas être utilisées pour confirmer une mutation, une autorisation ou un entitlement. Les quotas, idempotences, événements et audits conservent leur portée métier et ne sont pas réinitialisés par la région d'exécution.

Un `RegionalPlacementProvider` doit déclarer ses capacités et garanties de placement, de réplication, de chiffrement au repos et en transit, de gestion des clés, de suppression, de restauration, de révocation, de rétention et de transfert. La sélection est déterministe et la composition est bloquée lorsqu'une politique de résidence ne peut pas être démontrée. Les données et dérivés concernés incluent PostgreSQL, les objets, WAL et sauvegardes, réplicas, recherches, caches, fichiers temporaires, logs, traces, audits, événements, webhooks et copies offline.

La réplication active-passive peut être proposée par une capacité conforme. Une bascule exige une région de secours autorisée, une compatibilité de schéma et de contrats, un checkpoint vérifiable, un epoch ou fencing persistant empêchant l'ancien primaire d'écrire, ainsi qu'un audit. Une perte de contact, un désaccord d'epoch ou un risque de split-brain doit bloquer la bascule. L'actif-actif, le multi-primary et les transactions distribuées ne sont pas des garanties du socle et nécessitent une capacité spécialisée.

Une région indisponible ou un transfert non autorisé produit un état contrôlé, par exemple `REGION_UNAVAILABLE`, `PLACEMENT_UNSATISFIED`, `TRANSFER_FORBIDDEN` ou `FAILOVER_REQUIRED`, et ne doit pas déclencher un repli vers une région interdite. Une migration de tenant, une restauration inter-région ou une modification de politique est une opération explicite, versionnée, idempotente lorsque possible, reprenable et auditée. Les sauvegardes et restaurations doivent conserver les tombstones, rétentions, legal holds, clés, mappings, événements, Jobs, idempotences et obligations de gouvernance.

Les copies offline sont traitées comme des copies supplémentaires : leur présence doit être autorisée par la politique du tenant et le `DataGovernanceProfile`. Une copie locale ne doit pas permettre de contourner la résidence, la révocation, la suppression, le changement de scope ou l'expiration d'un accès. Les services de support, télémétrie et diagnostic appliquent les mêmes règles de minimisation et de transfert.

## 15. Exécution des Commands

Une Command est synchrone par défaut. Le mode asynchrone doit être déclaré explicitement dans le contrat public de la Command.

Une Command publique doit pouvoir transporter :

```text
command_id
command_type
command_version
subject
authentication_context éventuel
tenant_context
payload
correlation_id
causation_id
idempotency_key éventuelle
expected_version éventuelle
operation_id éventuel
```

Le dispatcher doit valider le type, la version, l'identité appelante, le contexte d'authentification, le contexte tenant, le payload, la version attendue et l'autorisation avant d'appeler le handler métier. Le handler exécute la mutation dans la frontière transactionnelle définie par le module propriétaire.

Une Command synchrone retourne un résultat ou une erreur métier après décision de la transaction. Une Command asynchrone persiste son opération et le ou les Jobs nécessaires dans la même frontière transactionnelle lorsque cela est possible, retourne un `operation_id` distinct du `job_id` et ne doit pas présenter la mutation comme acquise avant l'exécution et la validation correspondantes.

Les identifiants de corrélation et de causalité servent au suivi technique et fonctionnel. Ils ne remplacent pas l'identité numérique, le contexte tenant ou la clé d'idempotence.

### 15.1 Import, export et opérations en masse

`BulkOperation` est le contrat commun des traitements d'import et d'export. Il fournit un suivi persistant et ne devient jamais une autorité métier parallèle : les imports mutateurs utilisent les Commands du module propriétaire et les exports lisent des projections autorisées de la source de vérité.

```text
BulkOperation
├── operation_id
├── bulk_type             IMPORT | EXPORT
├── bulk_version
├── requested_by
├── tenant_context
├── scope_context éventuel
├── input_reference / output_reference
├── format
├── mapping_version éventuelle
├── commit_mode éventuel
├── source_snapshot ou watermark éventuel
├── idempotency_key éventuelle
├── progress
├── checkpoint éventuel
├── result_reference éventuelle
├── status
└── expires_at éventuel
```

Les états communs sont :

```text
REQUESTED
STAGED
VALIDATING
READY
RUNNING
COMPLETED
COMPLETED_WITH_ERRORS
FAILED
CANCELLED
EXPIRED
```

Les opérations qui dépassent le seuil d'exécution synchrone déclaré par la configuration sont asynchrones, exécutées par un ou plusieurs Jobs et suivies par `operation_id`. Le seuil n'est pas fixé par le Kernel. Une opération courte peut rester synchrone uniquement si le contrat garantit le même contrôle d'autorisation, d'idempotence et de gouvernance.

Les formats de référence du socle sont `CSV` et `NDJSON`. Le contrat reste extensible par des adapters pour XLSX, Parquet ou un format fournisseur ; un format supplémentaire doit déclarer son schéma, ses limites, son encodage, son mapping et ses garanties de validation. Un fichier important est stocké dans un `ObjectStorageProvider` privé et non conservé dans la mémoire d'un processus ou dans le filesystem local.

#### Import

Un import suit une phase de staging avant toute mutation :

```text
upload privé
    ↓
checksum, taille et type
    ↓
validation du schéma et du mapping
    ↓
prévisualisation ou VALIDATE_ONLY éventuel
    ↓
Commands du module propriétaire
    ↓
résultats, rejets et audit
```

Le fichier source est privé, soumis aux contrôles de taille, type, checksum, classification et éventuelle quarantaine. Le mapping est versionné ; les champs inconnus, ambigus ou non autorisés sont rejetés par défaut. Le tenant et le scope cible proviennent du contexte autorisé et ne peuvent pas être élargis par une valeur de payload. Une ressource d'un autre module est modifiée uniquement par son contrat public.

Le contrat doit distinguer les modes suivants :

```text
VALIDATE_ONLY       aucune mutation
ATOMIC              tout ou rien lorsque le module et la taille le permettent
ATOMIC_PER_CHUNK    validation et commit par unité de reprise
BEST_EFFORT         succès et rejets par élément, explicitement autorisé
```

`ATOMIC_PER_CHUNK` est le mode pratique par défaut pour les gros imports. `BEST_EFFORT` n'est accepté que si le module déclare les invariants préservés et fournit un rapport de rejets. Les conflits utilisent `REJECT` par défaut ; `CREATE_ONLY`, `UPDATE_ONLY` ou `UPSERT` doivent être explicitement autorisés par le module et le contrat d'import.

Chaque élément ou unité de reprise doit disposer d'une clé de déduplication lorsque la capacité le permet. Une même opération ou clé d'idempotence avec le même contenu restitue l'état ou le résultat persistant ; un contenu différent produit un conflit. Les checkpoints sont persistants, bornés et repris sans promettre `exactly-once`. L'annulation est coopérative et ne prétend pas annuler les chunks déjà validés.

#### Export

Un export est une lecture autorisée et contrôlée :

```text
demande autorisée
    ↓
projection et champs déclarés
    ↓
filter_authorized à la source
    ↓
snapshot logique ou watermark
    ↓
génération asynchrone
    ↓
fichier privé temporaire + manifeste
```

L'export n'utilise pas un index ou un cache comme source d'autorité. Les champs, relations, filtres, tris et périmètres sont déclarés par le module ; une sélection arbitraire de colonnes ou un `SELECT *` ne constitue pas un contrat d'export. Le snapshot logique ou le watermark doit permettre de diagnostiquer la cohérence du résultat sans maintenir une transaction longue lorsque cela n'est pas viable.

Le manifeste de résultat peut porter le format, la version du mapping, le périmètre tenant/scope, le snapshot ou watermark, le nombre d'éléments, le checksum, la classification, l'expiration et une référence de téléchargement. Le fichier est privé par défaut, accessible uniquement après nouvelle vérification des permissions et au moyen d'une référence ou URL temporaire contrôlée. La rétention du fichier, sa révocation et sa purge suivent la politique de gouvernance et de cycle de vie.

Les imports et exports doivent appliquer les profils de gouvernance des données. Une donnée non classifiée, une donnée protégée sans obligation résolue ou un flux sortant non déclaré doit être refusé. Les secrets ne peuvent jamais être importés depuis un fichier utilisateur ni inclus dans un export, un rapport de rejets, un événement ou un log. Les opérations relatives aux données personnelles peuvent réutiliser ce contrat, mais restent soumises aux règles propres à `DataSubjectRequest`.

Les événements de progression, de complétion, d'échec et de rejet sont versionnés et minimisés. Une mutation importée produit les événements métier requis par le module au travers de l'outbox ; l'opération de masse ne doit pas remplacer un événement par un payload agrégé ambigu. Les résultats, erreurs, checkpoints et références de fichiers sont persistants, corrélés, auditables et supprimés ou anonymisés selon les politiques applicables.

## 16. Outbox transactionnelle

Lorsqu'une mutation métier doit produire un événement publiable, le module ou service applicatif écrit l'événement dans une outbox au sein de la même transaction PostgreSQL que la mutation.

```text
Django
  ├── mutation métier
  └── événement dans l'outbox
          ↓ même transaction
        commit
          ↓
   publication asynchrone
```

Un événement présent dans l'outbox représente un événement dont la transaction métier a été validée. Un événement ne doit pas être publié avant ce commit lorsqu'il affirme qu'un fait métier est acquis.

L'outbox est une capacité générique du runtime et non une responsabilité du Kernel. Son contrat doit permettre au provider de persistance de garantir l'enregistrement transactionnel, la lecture des événements à publier, la reprise après interruption et le suivi de l'état de publication.

PostgreSQL est l'implémentation de référence initiale, mais le contrat ne doit pas empêcher un provider compatible lorsque les mêmes garanties sont conservées.

Les mutations de cycle de vie qui doivent être propagées écrivent dans la même frontière transactionnelle le changement de ressource, le tombstone éventuel et l'événement d'effacement. Un consommateur ne doit pas reconstruire une projection ou republier une ressource supprimée à partir d'un événement antérieur sans vérifier la version de suppression et le journal d'effacement.

Les événements de domaine internes et les événements d'intégration publics sont des contrats distincts. Ils peuvent partager l'outbox et le mécanisme de livraison, mais leur audience, leur schéma, leur politique de compatibilité et leur contenu sont déclarés séparément. Un événement d'intégration ne doit pas exposer un modèle privé ou un payload plus large que nécessaire.

## 17. Livraison des événements

La garantie de livraison des événements est `at-least-once`.

Un publisher doit pouvoir représenter au minimum :

```text
PENDING
PUBLISHED
RETRYING
FAILED
DEAD_LETTER
```

Après une erreur temporaire, la publication peut être retentée selon une stratégie de backoff. Après épuisement de la politique de retry, l'événement doit rester diagnostiquable dans un état d'échec ou être déplacé dans une dead-letter explicitement gérée.

Les consommateurs doivent être conçus pour supporter la réception multiple d'un même événement. Pixs ne promet pas `exactly-once` de bout en bout, notamment lorsqu'un événement est transmis à un système externe.

Une enveloppe d'événement doit pouvoir porter au minimum :

```text
event_id
event_type
event_version
producer_component
occurred_at
subject
tenant_context éventuel
correlation_id
causation_id éventuel
payload
```

L'ordre n'est garanti que selon le périmètre déclaré, par exemple un `aggregate_id` ou une partition. Une inbox ou une déduplication persistante, indexée au minimum par consommateur et `event_id`, doit protéger les effets secondaires. Un événement ne doit être considéré comme consommé qu'après l'enregistrement de cet état et de ses effets selon la frontière transactionnelle déclarée.

## 18. Idempotence des Commands

Toute Command susceptible d'être rejouée doit déclarer ou accepter une `idempotency_key`.

La déduplication utilise au minimum la clé composée suivante :

```text
tenant_id
subject_id
command_type
idempotency_key
```

Lorsque cette clé a déjà été traitée, le système doit retourner le résultat enregistré ou un état de traitement cohérent, sans exécuter une seconde fois la mutation. Une réutilisation de la même clé avec un payload différent est une erreur de conflit d'idempotence.

La conservation des clés, empreintes de payload, résultats et états de traitement doit être suffisamment durable pour couvrir la fenêtre de rejeu définie par la capacité concernée. La déduplication ne doit pas dépendre uniquement d'un cache mémoire.

Pour les événements, l'inbox ou le mécanisme équivalent conserve au minimum le consommateur, `event_id`, la version traitée, l'état de consommation, l'empreinte utile et les références de corrélation. Lorsque l'événement déclenche un Job dans la même source persistante, l'enregistrement de consommation et la création du Job doivent appartenir à une frontière transactionnelle commune. Un effet externe doit utiliser une clé d'idempotence ou une stratégie de déduplication propre au provider.

## 19. Queries

Une Query est une opération de lecture autorisée. Elle doit vérifier l'identité ou le sujet appelant, le contexte tenant et les permissions applicables avant de retourner une projection ou un résultat.

Une Query ne doit pas modifier l'état métier, publier un événement métier, créer implicitement une ressource, modifier un compteur fonctionnel, déclencher une migration ou contourner une ACL. Les caches, métriques et traces sont des effets techniques autorisés lorsqu'ils ne deviennent pas une source de vérité métier.

Une Query peut retourner des données projetées ou issues d'un index, mais la projection doit respecter les permissions et le contexte tenant du demandeur. Une donnée mise en cache ne doit jamais être servie à un sujet ou tenant non autorisé.

Les collections et recherches doivent utiliser `filter_authorized` ou un contrat équivalent afin que l'autorisation soit appliquée avant pagination et sérialisation. Une projection ou un index ne peut pas reconstituer une permission à partir d'un résultat déjà filtré ni servir une décision positive périmée.

Les requêtes normales excluent les ressources `SOFT_DELETED` et `PURGE_PENDING`, y compris lorsqu'elles utilisent un cache, un index ou une projection. Les lectures d'administration des données supprimées doivent être explicites, autorisées et auditées ; elles ne doivent pas exposer un payload effacé lorsque la politique l'interdit.

## 20. Configuration

Chaque composant déclare un schéma de configuration typé, validable et versionnable. Le schéma peut définir le type, le caractère requis, la valeur par défaut, les contraintes, le caractère secret et les règles de validation.

La résolution des valeurs suit cet ordre :

```text
schéma
  ↓
défaut du composant
  ↓
configuration statique de l'installation
  ↓
configuration runtime
  ↓
référence de secret
```

La source la plus prioritaire remplace la source la moins prioritaire. Une valeur fournie par une source non déclarée ne doit pas être prise en compte implicitement. Une configuration invalide doit empêcher l'activation ou le passage à `ready`.

Les adaptateurs Debian, Docker et développement local peuvent avoir des formats d'entrée différents, mais doivent produire le même modèle de configuration validé. La valeur effective peut être diagnostiquée par sa source et son statut sans exposer sa valeur lorsqu'elle est secrète.

Les feature flags sont une configuration runtime spécialisée, versionnée séparément de la configuration statique de composition. Les affectations peuvent varier entre installations, environnements, tenants et scopes sans reconstruire l'artefact. Elles doivent être modifiées par un contrat d'administration autorisé et audité ; leur source, leur version, leur durée de validité et leur statut doivent rester inspectables sans exposer de donnée sensible.

## 21. Secrets

Un secret est représenté par une référence et non par sa valeur dans la configuration fonctionnelle.

```text
Configuration
  └── référence de secret
          ↓
      SecretProvider
          ↓
       valeur en mémoire
```

Le contrat `SecretProvider` doit rester indépendant du mécanisme de stockage. Des providers peuvent utiliser un fichier protégé, une variable d'environnement, un secret Docker ou un gestionnaire externe.

Un secret doit être chargé au runtime, validé avant l'activation ou le passage à `ready` lorsque nécessaire, et ne doit apparaître dans aucun log, trace, audit, message d'erreur, manifest ou artefact. La rotation doit être supportée lorsque le provider et le composant consommateur le permettent.

Le runtime doit éviter de conserver les secrets plus longtemps que nécessaire et doit limiter leur exposition aux composants autorisés.

## 22. Lifecycle des composants

Les états de lifecycle sont des dimensions distinctes et ne doivent pas être réduits à un enum unique. Les phases de composition de référence sont :

```text
DISCOVERED
    ↓
VALIDATED
    ↓
RESOLVED
    ↓
LOADED
    ↓
ACTIVE
```

`DISCOVERED` signifie que le composant est identifié, `VALIDATED` que son manifest et ses préconditions sont valides, `RESOLVED` que ses dépendances et contrats sont satisfaits, `LOADED` que ses artefacts déclarés sont disponibles et `ACTIVE` qu'il est exposé par la composition.

Les états d'installation et d'exploitation sont indépendants :

```text
INSTALLED
ENABLED
CONFIGURED
READY
```

L'état de santé et de disponibilité est également indépendant :

```text
HEALTHY
DEGRADED
FAILED
DISABLED
```

Les opérations supportées sont explicitement représentées :

```text
discover → validate → install → enable → configure → start → ready
                                      └──────────────→ health check

disable
migrate
upgrade
uninstall
purge explicite
```

Une configuration, dépendance, contrat, contribution, point d'entrée ou contrainte de compatibilité invalide doit empêcher l'activation ou le passage à `ready`. Une défaillance doit rester observable et ne doit pas supprimer implicitement les données. Une extension optionnelle peut être isolée en `DEGRADED`, `FAILED` ou `DISABLED` ; une extension obligatoire non résolue ou incompatible bloque le périmètre concerné.

Une mise à niveau valide la composition, les contrats et les migrations avant activation de la nouvelle version. La purge est distincte de la désinstallation et nécessite une autorisation explicite. Le hot reload n'est permis que lorsqu'une capacité le déclare et en définit les garanties.

## 23. Jobs asynchrones

Le contrat générique `Job` représente un traitement pouvant être immédiat, différé, planifié, périodique, déclenché par un événement ou utilisé pour exécuter une Command asynchrone.

Un Job porte au minimum :

```text
job_id
job_type
job_version
payload
subject
tenant_context
correlation_id
causation_id
idempotency_key éventuelle
operation_id éventuel
scheduled_at éventuel
available_at éventuel
attempt_count
max_attempts éventuel
timeout éventuel
priority éventuelle
lease_owner éventuel
lease_expires_at éventuel
executor_identity éventuelle
last_error éventuelle
result_reference éventuelle
```

Ses états sont :

```text
PENDING
SCHEDULED
RUNNING
SUCCEEDED
RETRYING
FAILED
PAUSED
CANCELLED
DEAD_LETTER
```

Un Job n'est pas une autorité métier. Toute mutation déclenchée par un Job passe par une Command, avec validation, autorisation et transaction Django. Les handlers doivent être idempotents ou déclarer explicitement leurs limites. Les Jobs périodiques doivent être déclarés et versionnés. `operation_id` reste distinct de `job_id` : une opération peut produire plusieurs Jobs, et un Job peut être repris sans créer une nouvelle opération.

Les données nécessaires à la reprise — état, tentatives, échéances, résultats, leases et erreurs diagnostiquables — doivent être persistantes et compatibles avec la garantie `at-least-once`. Un worker acquiert un lease avec expiration et renouvellement bornés ; la perte du lease rend le Job reprenable après vérification de son état. Le scheduler utilise lui aussi un lease persistant et ne doit pas dépendre de la mémoire ou du filesystem local.

L'autorisation est évaluée à la mise en file puis réévaluée à l'exécution. Le Job conserve l'acteur initial, le `DigitalIdentity`, l'`AuthenticationContext` utile à l'audit et le `ScopeContext`, mais ne réutilise pas un contexte d'authentification expiré. Le worker ou le compte de service est l'exécuteur technique et ne peut pas élargir le périmètre de l'acteur initial.

Les erreurs métier non rejouables sont orientées vers `FAILED`, `CANCELLED` ou `DEAD_LETTER` selon le contrat. Les erreurs techniques temporaires peuvent utiliser un backoff et un nombre maximal de tentatives. Une reprise manuelle ou une replanification doit être explicitement autorisée, corrélée et auditée.

## 24. Notifications

Le flux générique d'une notification est :

```text
Event métier
    ↓
NotificationJob
    ↓
NotificationService
    ↓
ChannelProvider
```

Les canaux prévus sont :

```text
IN_APP
EMAIL
PUSH
SMS
WEBHOOK
```

Les canaux sont des capacités indépendantes. Aucun provider concret n'est imposé et la sélection suit les règles de résolution déterministe des providers.

Une notification doit pouvoir porter son identifiant, son type, sa version de modèle, son sujet, son contexte tenant, son canal, son destinataire, sa corrélation et sa clé de déduplication. Les modèles sont traduisibles et versionnés.

Les préférences et consentements doivent être évalués avant l'envoi. Les notifications transactionnelles et de sécurité peuvent suivre des règles distinctes des notifications marketing, mais cette distinction doit être explicite.

Les états de livraison sont :

```text
QUEUED
SENDING
SENT
DELIVERED
FAILED
CANCELLED
```

La livraison suit `at-least-once`, avec retries, backoff et déduplication. Une notification ne doit pas être envoyée avant le commit de la transaction métier qui la justifie. Le contenu d'une notification ne doit pas exposer de secret. Les notifications sensibles doivent être auditables.

## 25. Contrat API

HTTP/REST est le protocole API principal de Pixs. Les contrats d'API sont décrits par OpenAPI et versionnés indépendamment des implémentations Django ou TanStack.

Les routes tenant-scoped conservent le tenant dans leur chemin canonique, par exemple `/api/v1/tenants/{tenant_id}/resources`. Lorsqu'une ressource est portée par un scope enfant, le contrat doit déclarer comment le scope est résolu et, lorsque cela améliore la lisibilité ou l'unicité de la ressource, exposer un chemin explicitement scope-scoped. Un header, un champ de payload ou un paramètre non déclaré ne peut pas remplacer le `ScopeContext` canonique. Les routes platform-scoped restent distinctes.

Chaque route ou action sensible doit déclarer le niveau minimal d'`authentication_assurance`, d'`identity_assurance` et de `federation_trust`, ainsi que la fraîcheur maximale du contexte. Une exigence supérieure déclenche un step-up ou un refus explicite ; une permission d'affichage frontend ne peut pas satisfaire cette exigence.

Les Commands sont exposées comme opérations de mutation et les Queries comme opérations de lecture. Chaque route doit déclarer son contrat, son schéma d'entrée, son schéma de sortie, ses erreurs, ses exigences d'authentification, son `ScopeContext` et ses permissions.

Les erreurs publiques utilisent une enveloppe stable inspirée de Problem Details :

```json
{
  "error_code": "AUTHORIZATION_DENIED",
  "message": "Action non autorisée.",
  "details": {},
  "field_errors": [],
  "correlation_id": "..."
}
```

`error_code` est le code métier stable et versionné. `message` est destiné à la lecture humaine et ne constitue pas le contrat principal. `details` permet des informations structurées extensibles et `field_errors` est optionnel pour les validations d'entrée. Le statut HTTP décrit la classe de réponse de transport et complète l'enveloppe sans remplacer `error_code`. `correlation_id` doit permettre de relier la réponse aux traces, journaux et diagnostics autorisés.

Une réponse d'erreur ne doit contenir ni secret, ni stack trace, ni identifiant interne non nécessaire, ni détail de persistance. Les erreurs d'infrastructure doivent être normalisées par la frontière API et ne doivent pas révéler l'implémentation privée du module.

La version majeure d'une API est portée par son chemin public (`/api/v1/...`). Une évolution mineure ou corrective compatible ne change pas ce chemin et doit rester compatible avec le contrat de la version majeure. Une modification incompatible publie une nouvelle version majeure et son propre document OpenAPI. Les versions majeures peuvent coexister pendant une période de dépréciation explicitement documentée ; le retrait doit préciser la version cible, l'échéance et le remplacement éventuel.

L'authentification HTTP standard est portée par l'en-tête `Authorization: Bearer`. Un provider peut valider un token OAuth2/OIDC JWT ou opaque et doit produire un `AuthenticationContext` rattaché à une `DigitalIdentity`, avec ses niveaux d'assurance, sa validité et sa révocabilité. Les API keys sont réservées aux mécanismes explicitement déclarés pour les comptes de service et produisent au plus une assurance de base. Le mTLS peut être utilisé pour les identités `DEVICE` ou les comptes de service lorsque le provider le prend en charge.

L'autorisation ne doit être évaluée qu'après résolution de l'identité numérique, de l'`AuthenticationContext`, du `ScopeContext` et du contexte de requête. Un identifiant d'utilisateur présent dans le payload ou les paramètres ne modifie jamais le sujet authentifié. Une route sans authentification doit déclarer explicitement son caractère public dans son contrat API et appliquer malgré tout ses règles de validation et de limitation.

Pour une ressource tenant-scoped, le contexte canonique est porté par le chemin, par exemple `/api/v1/tenants/{tenant_id}/resources`. La frontière API résout ce tenant, vérifie la `TenantMembership` de la `DigitalIdentity` et transmet un contexte tenant immuable aux Commands, Queries, Events, Jobs et écritures d'audit. Un header tenant ou une valeur fournie dans le payload peut être rejeté ou traité comme une incohérence ; il ne remplace jamais le chemin canonique. Les routes platform-scoped ne doivent pas être implicitement rattachées à un tenant.

Les réponses JSON de succès utilisent l'enveloppe suivante :

```json
{
  "data": {},
  "meta": {},
  "links": {}
}
```

`data` contient la ressource, la collection ou le résultat de la Command. `meta` porte les informations complémentaires, notamment l'état de pagination, et `links` porte les liens de navigation ou de suivi. Les collections doivent utiliser un curseur opaque, stable et lié aux critères de tri déclarés ; un curseur ne doit pas révéler la requête interne ni permettre de franchir une frontière tenant. Une Command asynchrone répond avec `202 Accepted`, un `operation_id` et une URL de suivi vers l'état persistant de l'opération. La réponse ne doit pas exposer directement un modèle Django ou une structure de persistance.

Les paramètres de filtre et de tri font partie du contrat OpenAPI et doivent être validés avant l'exécution de la Query. Chaque module déclare les champs filtrables, les opérateurs autorisés, les types et les champs triables. Le tri doit être total et stable, avec un critère secondaire déterministe tel que l'identifiant UUIDv7. La taille de page est plafonnée côté serveur et le curseur encode uniquement un état de pagination validé. Le client ne peut pas fournir de fragment SQL, d'expression ORM ou de nom de champ non déclaré. Une recherche textuelle, sémantique ou plein texte est une capacité séparée, avec ses propres limites, index et garanties.

Une ressource qui expose sa version de concurrence peut produire un `ETag` stable dérivé de cette version. `If-None-Match` permet de répondre `304 Not Modified` pour une lecture conditionnelle lorsque le cache est autorisé. `If-Match` doit être exigé pour les mutations où une écriture obsolète risquerait d'écraser une modification concurrente ; l'échec de la précondition répond `412 Precondition Failed`. Un conflit métier distinct répond `409 Conflict`. Les règles `Cache-Control`, la portée du cache et la sensibilité des données doivent être déclarées par route. Un cache partagé ne doit pas être utilisé implicitement pour une réponse sensible ou tenant-scoped.

Une route qui expose une Command rejouable doit déclarer l'en-tête `Idempotency-Key` et préciser s'il est obligatoire. La frontière API calcule l'identité de la demande avec le contexte `tenant_id`, `subject_id`, `command_type` et la clé, conformément à la convention générale d'idempotence. Pour une clé déjà traitée avec le même payload, elle restitue le statut, les en-têtes pertinents et le corps enregistrés, ou l'état persistant de l'opération asynchrone. Un payload différent pour la même clé répond `409 Conflict`. L'enregistrement d'idempotence doit être persistant, lié au tenant et soumis à une politique de rétention documentée. `GET`, `HEAD` et `OPTIONS` ne doivent pas dépendre de cette clé.

La limitation de débit est une capacité déclarée par route, méthode ou type d'opération. La clé de quota doit respecter le contexte de sécurité : identité numérique et tenant lorsqu'ils sont connus, compte de service pour ses consommations propres, ou adresse IP uniquement pour une route anonyme. Un provider peut appliquer plusieurs fenêtres ou algorithmes, mais doit exposer un refus uniforme `429 Too Many Requests`, l'enveloppe d'erreur API et `Retry-After` lorsque possible. Les quotas ne doivent pas permettre à un tenant ou une identité de consommer silencieusement la capacité d'un autre. Les opérations d'authentification, de recherche coûteuse, de mutation et de lecture peuvent avoir des politiques différentes.

Un adapter webhook peut consommer les événements publiables de l'outbox après le commit de la transaction source. L'enveloppe externe doit être versionnée et contenir au minimum `event_id`, `event_type`, `event_version`, `tenant_id` lorsque pertinent, `occurred_at`, `payload`, `correlation_id` et `causation_id` lorsque disponibles. Chaque endpoint possède une configuration, une destination validée et un secret référencé par le système de secrets. La signature doit couvrir le contenu transmis et des informations permettant d'empêcher ou de détecter le rejeu. La livraison est `at-least-once` : les tentatives, délais, réponses, échecs et dead-letters sont persistants et diagnostiquables. Une rotation de secret doit permettre une période de transition contrôlée. Un payload webhook ne doit pas exposer de donnée sensible qui n'est pas nécessaire au consommateur.

Un adapter d'ingestion reçoit les webhooks entrants sur une frontière séparée de l'API métier. Il vérifie la signature, la fenêtre temporelle et l'identifiant externe avant d'accepter le message. L'identifiant du provider et l'empreinte du payload sont enregistrés dans un mécanisme d'idempotence adapté afin de détecter les replays et les incohérences. Le message brut, lorsqu'il est conservé pour diagnostic, doit être soumis à une rétention, une protection d'accès et une politique de minimisation des données. Après validation, l'adapter produit une Command ou un événement interne versionné ; il ne modifie pas directement les modèles métier. L'identité numérique, le tenant et le provider d'origine doivent être résolus explicitement, sans confiance implicite dans un champ du payload. Les messages invalides, non rattachables ou définitivement échoués sont diagnostiquables et orientés vers une dead-letter.

CORS est refusé par défaut. Les origines, méthodes, headers et credentials autorisés doivent être déclarés par environnement ; `*` est interdit lorsqu'une réponse autorise les credentials. Les pré-requêtes doivent être évaluées avec les mêmes frontières d'authentification, de tenant et de rate limiting que les requêtes réelles. Une authentification par cookie active la protection CSRF et les attributs de cookie adaptés. Une authentification Bearer sans cookie ne doit pas être traitée comme une session CSRF, mais reste soumise à CORS, à l'authentification et à l'autorisation normales.

Chaque route déclare un budget de taille de requête, de taille de réponse et de durée d'exécution, avec des valeurs distinctes lorsque le transport reçoit du JSON, du multipart ou un upload. La frontière API rejette un corps supérieur à sa limite avec `413 Content Too Large` avant de lancer la logique métier. Un traitement qui dépasse son budget doit être annulé proprement lorsque cela est possible ; s'il est intrinsèquement long, il doit être exposé comme une Command asynchrone répondant `202 Accepted` et fournissant un suivi persistant. `408 Request Timeout` décrit un délai d'attente côté requête ou client, tandis que `504 Gateway Timeout` décrit un délai d'attente d'une dépendance ou d'un intermédiaire. Les limites doivent être observables sans enregistrer le contenu sensible du payload.

Le format par défaut des échanges est `application/json; charset=utf-8`. La frontière API doit vérifier `Content-Type` pour les corps reçus et `Accept` pour la représentation demandée. Elle répond `415 Unsupported Media Type` lorsqu'elle ne peut pas lire le format envoyé et `406 Not Acceptable` lorsqu'elle ne peut pas produire une représentation acceptée. Les dates et timestamps sont sérialisés en RFC 3339 avec une référence UTC. Les UUID, identifiants externes et nombres décimaux doivent conserver leur précision et leur représentation contractuelle. `Accept-Language` peut sélectionner une traduction de `message` ou d'un contenu destiné à l'humain ; il ne modifie ni `error_code`, ni les noms de propriétés, ni la forme OpenAPI. Une route ne doit pas changer silencieusement de contrat selon le frontend appelant.

OpenAPI constitue la source de vérité des contrats API publics. Un test de contrat doit vérifier au minimum les routes, méthodes, paramètres, schémas d'entrée et de sortie, statuts HTTP, enveloppes de succès et d'erreur, exigences d'authentification, contexte tenant et limites déclarées. Les exemples de requêtes et réponses sont versionnés avec le contrat. Un contrôle de compatibilité compare toute évolution à la version majeure publiée et bloque les ruptures qui ne sont pas accompagnées d'une nouvelle version majeure. Les SDK, clients typés et documentations générés sont des artefacts dérivés et ne doivent pas être modifiés pour masquer une divergence du contrat.

Les contrats d'événements sont versionnés séparément des contrats HTTP. Une représentation compatible avec AsyncAPI peut décrire les types, versions, schémas, producteurs, consommateurs, canaux, ordre, garanties de livraison et politiques de rejeu sans imposer de broker ni de transport au Kernel. Les événements d'intégration publics sont dérivés de contrats explicites et ne doivent pas exposer les modèles privés, secrets ou données non nécessaires à leurs consommateurs. Les webhooks sortants sont des adapters de ces événements ; les webhooks entrants passent par une frontière d'ingestion qui vérifie signature, fraîcheur, identifiant externe et rejeu avant de produire une Command ou un événement interne.

WebSocket et SSE sont des transports optionnels réservés aux capacités réactives. GraphQL et RPC peuvent être ajoutés comme adapters compatibles, mais ne sont pas requis par le Kernel ni par le contrat API principal.

Une API ne doit jamais exposer directement les modèles privés, repositories ou détails de persistance d'un module. Elle utilise les interfaces publiques, Commands, Queries, services et schémas déclarés.

### 25.1 SDK et Developer Kit

Les SDK officiels initiaux sont TypeScript et Python. Ils sont des clients des contrats publics et non des projections des modèles Django. La génération s'appuie sur les documents OpenAPI, les contrats événementiels compatibles avec AsyncAPI et les JSON Schemas publics ; les types, clients bas niveau, exemples et métadonnées de contrat sont produits de manière déterministe. Une façade ergonomique peut être maintenue au-dessus du code généré, mais elle ne peut pas modifier la sémantique, les garanties ou les versions du contrat source.

```text
contrats OpenAPI / AsyncAPI / JSON Schema
                    ↓
        validation et compatibilité
                    ↓
          génération déterministe
                    ↓
        client typé bas niveau
                    ↓
       façade ergonomique optionnelle
```

Le client partagé doit fournir, lorsque le contrat le prévoit, le transport HTTP ou événementiel, les erreurs typées, les enveloppes `data`/`meta`/`links`, la pagination par curseur, le `TenantContext`, le `ScopeContext`, la corrélation, les `Idempotency-Key`, le suivi des `operation_id` et des `BulkOperation`, ainsi que les limites et budgets déclarés. Le contexte de tenant et de scope est fourni explicitement, immuable pendant la requête et ne peut pas être remplacé par un champ de payload ou une valeur globale cachée.

L'authentification est injectée par un provider ou une fonction de résolution de credential. Le SDK ne devient pas une autorité d'identité et ne doit pas imposer un mécanisme de stockage des tokens. Dans le navigateur, les tokens et credentials ne sont pas persistés localement par défaut ; une application qui choisit une persistance doit l'assumer explicitement et respecter les règles de sécurité du projet. Les SDK serveur peuvent utiliser des credentials de service ou des flux OAuth selon les contrats et providers déclarés, sans afficher les secrets.

Une mutation n'est automatiquement rejouée que si une clé d'idempotence et le contrat l'autorisent. Les retries sont bornés, soumis à un backoff déclaré et distinguent les erreurs techniques rejouables des erreurs métier. Un traitement asynchrone reste dans un état en cours tant que le suivi persistant ne confirme pas son résultat ; le SDK ne transforme pas un `202` en succès métier. Les webhooks entrants et sortants disposent d'un utilitaire de signature, de vérification de fraîcheur et de détection du rejeu lorsque le contrat le prévoit.

Le Developer Kit est distinct des clients runtime. Il fournit le scaffolding, la validation du `component.toml`, la génération des contrats et clients, la vérification des capacités et dépendances, le contrôle des imports publics, la compatibilité SemVer et les tests de conformité. La CLI officielle réutilise ces bibliothèques pour les commandes de création, inspection, validation, génération, test, compatibilité et diagnostic ; ses sorties et codes d'erreur sont stables et ne contiennent pas de secret.

Les packages SDK et outils sont versionnés par `sdk_version`, avec des contraintes de compatibilité explicites envers les versions d'API, de contrats, de composants et de schémas. La publication vers npm, PyPI ou un autre registry est un adapter ; elle ne doit pas être nécessaire pour construire ou exécuter Pixs, et une installation runtime de code distant est interdite par défaut. Les fixtures, exemples et rapports de conformité sont synthétiques, reproductibles et dépourvus de données de production.

### 25.2 Quotas et entitlements

Un entitlement exprime la disponibilité contractuelle d'une capacité ou d'une limite pour un sujet de déploiement. Un quota exprime une consommation quantitative autorisée. Ils sont distincts de la capacité composée, de l'autorisation, de l'authentification et du feature flag : un entitlement ne prouve pas l'identité, un quota ne donne pas de permission et un flag ne peut pas créer un entitlement.

Le Kernel ne porte pas la facturation, les abonnements ou les plans commerciaux. Il définit les contrats de résolution et d'application. Un `EntitlementProvider` peut fournir un snapshot ou une décision issue d'une licence, d'un abonnement, d'une politique d'installation ou d'un système externe ; il doit être versionné, corrélé, révocable et ne peut pas écrire directement dans les modèles métier Pixs.

Le modèle logique d'un entitlement est le suivant :

```text
Entitlement
├── entitlement_id
├── entitlement_key
├── subject_type       INSTALLATION | PLATFORM | TENANT | SCOPE
├── subject_id
├── tenant_id éventuel
├── scope_id éventuel
├── value ou limite contractuelle
├── status              SCHEDULED | ACTIVE | EXPIRED | SUSPENDED | REVOKED
├── source_reference
├── entitlement_version
├── valid_from
├── expires_at éventuel
└── revision
```

Les entitlements sont rattachés par défaut à l'installation, à la plateforme ou au tenant. Un rattachement à un scope enfant est possible uniquement si le contrat le prévoit explicitement et ne peut pas élargir les capacités du tenant. Les entitlements utilisateurs ne sont pas une dimension implicite. La décision expose conceptuellement `allowed`, la cause, la version, la portée et la période de validité, sans révéler la politique commerciale ou des données confidentielles à un appelant non autorisé.

Une politique de quota doit déclarer au minimum :

```text
QuotaPolicy
├── quota_id
├── quota_policy_version
├── dimension          REQUESTS | RATE | CONCURRENCY | BYTES | OBJECTS | ROWS | JOBS | OPERATION_COST
├── unit
├── subject_scope      INSTALLATION | PLATFORM | TENANT | SCOPE | IDENTITY | IP | OPERATION
├── limit
├── period ou lifetime
├── aggregation        COUNTER | WINDOW | CONCURRENCY | RESERVATION
├── reset_at éventuel
└── status
```

Les unités sont explicites et doivent éviter les flottants ambigus pour les compteurs et coûts. Les limites de débit ou de concurrence courte sont distinguées des quotas cumulés sur une fenêtre ou une durée de vie. Plusieurs politiques peuvent s'appliquer à une même opération ; elles sont évaluées simultanément et l'opération est refusée dès qu'une limite applicable n'est pas disponible.

Le `QuotaProvider` expose conceptuellement les opérations suivantes :

```text
check(context, request)       → décision sans réservation
reserve(context, request)     → réservation atomique
commit(reservation, actual)   → consommation effective
release(reservation, unused)  → libération contrôlée
```

Une réservation possède un identifiant stable, une clé d'idempotence, une opération, un contexte tenant/scope, une estimation, un état, une échéance et une référence de politique. `reserve`, `commit` et `release` doivent être persistants et idempotents. Une même clé avec une demande différente produit un conflit explicite. Un retry, une reprise ou une annulation ne doit pas doubler la consommation ; la différence entre estimation et usage réel est réconciliée selon la politique.

PostgreSQL constitue le provider de référence pour les compteurs durables, décisions et réservations. Un provider spécialisé de haute fréquence est autorisé s'il garantit l'atomicité, la persistance, la déduplication, l'expiration, la reprise et la cohérence tenant/scope nécessaires. Un cache local peut accélérer une lecture d'entitlement ou de politique avec une durée et une invalidation bornées, mais il ne constitue jamais l'autorité et ne peut pas maintenir une décision après expiration, suspension ou révocation.

La résolution d'une opération suit conceptuellement :

```text
capacité composée et disponible
              ↓
entitlement valide
              ↓
autorisation de l'identité sur la ressource
              ↓
feature flag compatible, s'il s'applique
              ↓
réservation des quotas nécessaires
              ↓
exécution et réconciliation
```

Une indisponibilité, incohérence ou expiration échoue fermé pour les mutations, actions sensibles, opérations coûteuses, données protégées, Jobs et opérations bulk. Un dépassement récupérable peut répondre `429 Too Many Requests` avec un `Retry-After` lorsque le renouvellement est connu ; un entitlement absent ou révoqué utilise un code d'erreur distinct. Les réponses et SDK ne doivent exposer que la décision et les limites nécessaires au consommateur autorisé.

Les APIs, Commands asynchrones, Jobs, imports et exports vérifient les entitlements et quotas à la création puis au point d'exécution lorsque la durée ou la consommation le justifie. Une opération bulk réserve notamment les octets, lignes, concurrence et Jobs nécessaires ; elle libère les réservations non consommées et conserve l'audit des unités effectivement engagées. Les compteurs, décisions et références de réservation portent le `ScopeContext`, l'acteur, la corrélation et la causalité applicables sans conserver le payload sensible.

### 25.3 Offline-first et synchronisation locale conditionnelles

L'offline-first est une capacité optionnelle exposée par un contrat `OfflineSyncCapability`. Elle est déclarée et résolue par composant, ressource, tenant et scope ; elle ne constitue pas un mode global du runtime et son absence ne modifie pas le comportement connecté. Le contrat ne doit pas imposer Electric, une base navigateur, IndexedDB, un service worker ou un provider local particulier.

Une capacité offline-first déclare au minimum :

```text
OfflineSyncCapability
├── capability_id
├── capability_version
├── resource_types
├── read_projections
├── command_types éventuels
├── allowed_tenant_scopes
├── allowed_confidentiality
├── local_retention
├── encryption_policy
├── offline_access_lease_policy éventuelle
├── max_staleness
├── local_schema_version
├── sync_protocol_version
├── conflict_policy
└── revocation_invalidation_policy
```

Les projections locales sont des répliques non autoritatives. Elles sont liées au contexte déclaré et peuvent porter les états `ONLINE`, `OFFLINE`, `CATCHING_UP`, `STALE`, `CONFLICT`, `REVOKED` et `PURGED`. Elles doivent conserver un curseur ou watermark serveur, une version de projection, une date de dernière synchronisation et une échéance de fraîcheur lorsque ces informations sont nécessaires à la décision d'affichage. La connectivité détectée par le client n'est qu'un signal de transport.

Le modèle logique d'une réplique locale est le suivant :

```text
LocalReplica
├── replica_id
├── subject_reference
├── device_reference éventuelle
├── TenantContext
├── ScopeContext
├── projection_version
├── local_schema_version
├── server_cursor éventuel
├── last_sync_at éventuel
├── stale_at éventuel
├── status
└── revision
```

Le modèle logique d'une Command créée hors ligne est le suivant :

```text
OfflineCommand
├── offline_command_id
├── command_type
├── command_version
├── operation_id éventuel
├── idempotency_key
├── actor_reference
├── TenantContext
├── ScopeContext
├── payload_reference ou payload chiffré selon la politique
├── payload_digest
├── created_at
├── expires_at éventuel
├── state              PENDING | SUBMITTED | APPLIED | REJECTED | CONFLICT | EXPIRED | REVOKED
└── last_sync_error éventuel
```

Une `OfflineCommand` est une intention et non une mutation confirmée. Le client peut afficher un état provisoire, mais seul le backend peut produire l'effet métier, l'Event de domaine et l'entrée d'outbox correspondants. À la reconnexion, le serveur authentifie à nouveau l'appel, résout le `ScopeContext`, réévalue l'autorisation, l'entitlement, les quotas, la concurrence et la gouvernance, puis appelle la Command Django du module propriétaire. Un `AuthenticationContext` ou une permission expiré ne peut pas être réutilisé comme preuve.

La soumission utilise une clé d'idempotence et un identifiant stables. Les retries, replays, redémarrages et pertes de connexion suivent `at-least-once` ; ils ne doivent pas produire deux effets métier confirmés. Une opération ne peut être marquée `APPLIED` qu'après confirmation serveur. Les Events locaux restent limités à l'interface, au suivi de synchronisation et aux états provisoires ; ils ne remplacent ni l'Event Bus, ni l'inbox/outbox, ni les garanties transactionnelles.

La synchronisation locale suit conceptuellement :

```text
snapshot / changements autorisés du serveur
                ↓
        LocalReplica versionnée
                ↓
     lecture éventuellement STALE
                ↓
OfflineCommand PENDING éventuelle
                ↓ reconnexion
authentification + ScopeContext + autorisation
                ↓
entitlement + quota + concurrence + gouvernance
                ↓
       Command Django / PostgreSQL
                ↓
     Event / outbox / projection
                ↓
      checkpoint et réconciliation
```

Les conflits sont déclarés par ressource et ne sont jamais résolus silencieusement. Les stratégies permises sont `REJECT`, `MANUAL_REVIEW`, `DOMAIN_MERGE` et, lorsque la perte est acceptable et documentée, `LAST_WRITE_WINS`. Une résolution locale ne peut pas publier un Event de domaine, élargir un scope, prolonger un entitlement ou confirmer une réservation de quota.

La persistance locale respecte le `DataGovernanceProfile`. `PUBLIC` et `INTERNAL` peuvent être autorisés par défaut lorsque la capacité le déclare ; `CONFIDENTIAL` exige une politique de stockage sécurisée et explicite ; `RESTRICTED` et `SENSITIVE_PERSONAL` sont refusés par défaut. Les secrets, tokens, credentials et preuves d'authentification brutes ne sont jamais stockés localement. Une projection non publique peut exiger un `OfflineAccessLease` borné, lié au sujet, à l'appareil, au tenant et au scope, sans remplacer la réévaluation serveur.

Un changement de tenant ou de scope, une déconnexion, une expiration, une révocation, un tombstone, une demande d'effacement ou une expiration de rétention doit invalider ou purger les répliques et Commands concernées. Les caches locaux ne doivent pas masquer une révocation ou une version dépassée. Les quotas et entitlements sont résolus côté serveur à la soumission ; les imports, exports, opérations bulk, purges et actions sensibles sont refusés hors ligne par défaut.

La synchronisation locale est distincte d'une synchronisation externe. Elle ne crée pas de mode `EXTERNAL` ou `EXPLICIT_BIDIRECTIONAL` et ne confère pas au client local une autorité concurrente. Electric peut fournir un transport de changements pour une capacité compatible, mais les mêmes contrats de source de vérité, d'autorisation, de cycle de vie, de gouvernance et de conflit restent applicables.

## 26. Extension frontend

Le frontend de référence utilise TanStack, mais les frontières d'extension sont définies par des contrats frontend publics et versionnés plutôt que par les imports ou l'arborescence interne du shell.

Le shell expose également un `ScopeContext` en lecture seule, comprenant le tenant racine et le scope enfant éventuel. Les clés de cache, projections et états locaux doivent intégrer ce contexte lorsqu'il est applicable. Un changement de tenant ou de scope annule ou invalide les données dépendantes avant d'exposer le nouveau contexte ; une extension ne peut pas le modifier ni élargir son périmètre.

Un composant peut déclarer dans son manifest des contributions de types suivants :

```text
ROUTE          route frontend et exigences d'accès
PAGE           page ou écran rattaché à une route
NAVIGATION     entrée de navigation
COMPONENT      composant réutilisable
FORM           formulaire et schéma de présentation
TRANSLATION    ressources de traduction
UI_PERMISSION  visibilité ou activation d'un élément
UI_SLOT        point d'insertion déclaré par le shell
```

Chaque contribution possède un identifiant stable, un propriétaire, une version de contrat, des dépendances éventuelles et des conditions d'activation. Le registre frontend valide les identifiants, les versions, les collisions, les permissions d'affichage, les exigences de module et la compatibilité avec le shell avant exposition.

La modularité frontend est portée par les composants `MODULE` et `SUBMODULE` du modèle commun ; aucun type `FRONTEND_MODULE`, `FRONTEND_SUBMODULE`, registre ou lifecycle distinct ne doit être introduit. La section `[frontend]` d'un manifest exprime une facette du composant propriétaire. Un sous-module qui porte une facette frontend reste donc découvert, validé, résolu et diagnostiqué par les mécanismes communs, avec la même relation de parenté, les mêmes contraintes SemVer et les mêmes états que sa partie non frontend.

Un sous-module frontend déclare ses propres contributions, points d'entrée, contrats, traductions et dépendances. Il consomme uniquement les façades publiques du shell, du Design System, de son parent ou d'autres composants explicitement requis. Le parent ne rend ni une contribution enfant active ni son état accessible par convention d'arborescence ; toute intégration entre parent et enfant passe par une contribution, un slot, un service frontend ou un contrat UI public, namespacé et versionné.

Le shell conserve la responsabilité du lifecycle d'interface, du routage global, de l'authentification, du contexte tenant, de la gestion des erreurs, du chargement, du Design System et des garde-fous de sécurité. Une extension peut demander une donnée ou une action au travers des APIs, Commands, Queries et contrats UI publics ; elle ne peut pas modifier directement l'état métier, les ACL ou les modèles backend.

La résolution des contributions doit être déterministe, indépendante de l'ordre des imports et reproductible entre développement, build et runtime. Le lazy loading est une optimisation déclarée par la contribution et ne doit pas modifier les règles d'autorisation. Un adapter TanStack traduit les contrats frontend génériques en routes, composants et mécanismes de chargement propres à TanStack.

La résolution parcourt le graphe complet des modules et sous-modules qui déclarent une facette frontend. Elle vérifie les dépendances de composant et de contribution, les façades publiques, les contraintes de version, les collisions et la compatibilité avec le shell avant de produire une composition unique. Un sous-module optionnel non résolu ne retire que les contributions qui en dépendent ; un sous-module ou une contribution obligatoire non résolu rend le périmètre concerné non composable. L'ordre de découverte, le chemin physique et les imports ne constituent jamais des règles de rattachement ou de priorité.

La distribution de référence est une composition au build. Le composant frontend d'un module est livré avec ses sources ou artefacts, son manifest et ses contraintes de compatibilité avec le shell. Le build résout les contributions et génère les bundles ou chunks nécessaires dans l'artefact Pixs. Le runtime ne doit pas exécuter de téléchargement, d'installation de dépendance ou d'évaluation de code distant pour activer une extension. Le lazy loading ne fait que différer le chargement d'un chunk déjà livré. Un adapter de module distant pourra définir une autre stratégie, mais devra conserver les contrats, signatures, versions, permissions et garanties de sécurité du registre frontend.

Les extensions frontend consomment uniquement les API publiques versionnées. Le shell expose deux abstractions distinctes :

```text
QueryClient    lecture via Query et API publiques
CommandClient  mutation via Command et API publiques
```

Toute clé de cache frontend doit intégrer le scope lorsqu'il est applicable, en plus du tenant, de l'identité, de la ressource et des paramètres validés.

Un adapter peut générer les clients typés à partir d'OpenAPI. TanStack Query peut implémenter la gestion de l'état serveur, du cache, de l'invalidation et des retries, mais ne devient pas la source de vérité métier. Une clé de cache doit être déterminée par la version d'API, le tenant, l'identité lorsque pertinente, la ressource, les filtres, le tri et les autres paramètres validés. Une réponse ou projection Electric ne peut être utilisée que si la capacité déclare la réactivité et ne peut jamais remplacer la vérification d'autorisation backend. Les mutations optimistes représentent un état d'interface provisoire et doivent être réconciliées avec le résultat de la Command.

Le shell expose un contexte de session en lecture seule aux extensions :

```text
DigitalIdentity   identité authentifiée ou absence d'identité
User              utilisateur associé éventuellement
Tenant            tenant courant ou contexte plateforme
ScopeContext      tenant racine et scope enfant éventuel
Authentication    niveaux d'assurance et fraîcheur exposables
UIPermissions     permissions utiles à l'affichage
SessionState      initialisation, active, expirée, révoquée, erreur
```

Une extension ne doit pas accéder aux tokens bruts, les décoder ou les persister. Le token d'accès peut rester en mémoire pendant la session ; le renouvellement navigateur utilise, lorsque nécessaire, une session de renouvellement portée par un cookie `HttpOnly`, `Secure` et `SameSite` compatible avec la politique CSRF. `localStorage` et `sessionStorage` ne doivent pas contenir de token d'accès ou de renouvellement. Les guards de route et permissions UI sont des optimisations d'expérience, jamais des décisions d'autorisation. Lorsqu'un tenant ou un scope courant change, le shell doit annuler ou invalider les requêtes, caches, projections et états locaux liés à l'ancien contexte avant d'exposer le nouveau. Le niveau d'assurance peut être affiché ou utilisé pour guider un step-up, mais ne constitue jamais une décision d'autorisation côté frontend.

Le registre et le shell suivent le lifecycle propre à chaque extension :

```text
DISCOVERED → RESOLVED → LOADED → ACTIVE
                              ├→ DEGRADED
                              ├→ FAILED
                              └→ DISABLED
```

`DISCOVERED` signifie que la contribution est connue, `RESOLVED` qu'elle est compatible et sélectionnée, `LOADED` que ses artefacts sont disponibles et `ACTIVE` qu'elle est exposée. `DEGRADED` indique qu'une capacité non essentielle n'est pas disponible ; `FAILED` indique une erreur d'initialisation ou d'exécution ; `DISABLED` indique une désactivation explicite ou résultant d'une dépendance. Une extension obligatoire en `FAILED` ou `DISABLED` peut empêcher le shell de devenir `ready`. Une extension optionnelle doit être isolée par une boundary d'erreur, retirer ses contributions invalides et laisser le reste de l'interface fonctionner. Les transitions, raisons, versions et corrélations sont observables sans exposer de secret.

Le build frontend établit la confiance des extensions avant distribution. Le manifest, les dépendances et les artefacts doivent être associés à des empreintes vérifiables et à une provenance traçable. Le shell applique une CSP restrictive, interdit l'évaluation dynamique de code et limite les scripts inline aux exceptions explicitement nécessaires. Les bundles et chunks chargés doivent être protégés contre une substitution non prévue. Un adapter d'extension distante doit vérifier l'autorisation, la version, la provenance, la signature ou l'intégrité et la compatibilité avant chargement ; l'activation distante ne peut pas être implicite. Une extension embarquée dans le bundle possède les privilèges du shell et ne doit donc pas être traitée comme isolée. Pour du code non pleinement fiable, l'isolation doit être fournie par un iframe ou un sandbox avec une API minimale, sans accès aux secrets, au stockage de session ou aux APIs privées du shell.

Les extensions disposent d'un bus UI fourni par le shell pour les notifications et synchronisations d'interface. Un événement UI public doit disposer d'un identifiant namespacé, d'une version, d'un schéma de payload, d'un producteur, de consommateurs autorisés et de garanties documentées concernant l'ordre, la répétition et la durée de vie. Le bus UI ne remplace pas le bus d'événements métier, l'outbox ou les Commands backend. Une extension peut publier un événement d'affichage ou demander une action publique au shell, mais le shell doit refuser les actions non déclarées et le backend doit réévaluer toute permission sensible. Le partage d'état se fait par contrats de lecture ou d'action ; un store global mutable accessible à toutes les extensions est interdit par défaut.

Le shell distingue les modes de rendu suivants :

```text
CSR       rendu client, mode de référence pour les espaces authentifiés
SSR       rendu serveur ponctuel pour une route déclarée
STREAMING rendu serveur progressif lorsqu'il est supporté par le shell
SSG       génération statique pour un contenu public et stable
```

Une route déclare son mode de rendu, ses besoins d'hydratation et les données autorisées au pré-rendu. Le CSR ne doit pas être traité comme une garantie d'autorisation. Le SSR et le streaming ne doivent pas sérialiser de token, secret, permission sensible ou donnée tenant dans le HTML au-delà de ce qui est explicitement nécessaire au contexte courant. Le SSG ne peut consommer que des données publiques, versionnées et compatibles avec la durée de validité de l'artefact. Une extension qui déclare SSR ou streaming doit être déterministe entre rendu serveur et hydratation client, ou déclarer précisément ses limites.

Une contribution de routage doit déclarer un `route_id` namespacé, son chemin, son composant de rendu, son mode de rendu, son périmètre d'accès, ses paramètres, ses redirections éventuelles, ses exigences de navigation et sa version de contrat. Le registre refuse deux chemins ou identifiants incompatibles et interdit à un module de masquer une route du shell sans override public explicitement versionné. Les routes `PUBLIC`, `AUTHENTICATED`, `TENANT_SCOPED` et `PLATFORM_SCOPED` sont des catégories distinctes. Le serveur ou l'adapter de distribution doit renvoyer le shell approprié pour un deep link, puis laisser le routeur valider le contexte et les permissions d'affichage. Les changements de chemin doivent fournir une redirection ou une stratégie de migration documentée ; ils ne doivent pas casser silencieusement les liens enregistrés.

Le graphe de dépendances frontend doit respecter les dépendances de composants, mais il ne doit pas exposer leurs implémentations privées. Les imports autorisés sont ceux du shell, du Design System, des APIs frontend communes et des façades publiques d'extensions explicitement déclarées. Une façade est un contrat de contribution ou de service frontend versionné ; elle ne doit pas rendre accessible un store privé ou un token. Le registre vérifie les dépendances obligatoires et optionnelles, les contraintes SemVer et l'absence de cycle avant résolution. Une dépendance optionnelle manquante place seulement la contribution concernée en `DEGRADED` ou `DISABLED` selon sa déclaration ; une dépendance obligatoire non résolue empêche `ACTIVE`.

Le manifest `component.toml` est la source déclarative unique du composant backend et frontend. Sa section optionnelle `[frontend]` peut préciser l'activation frontend, la version minimale ou compatible de l'API du shell et la liste des contributions. Une contribution doit au minimum déclarer :

```text
type       type de contribution frontend
id         identifiant namespacé stable
entry      point d'entrée résolu dans le composant
version    version du contrat de contribution
requires   contrats ou contributions requis, lorsque nécessaire
```

Les chemins d'entrée sont résolus relativement au composant après validation du manifest. La présence d'un fichier ou d'un répertoire frontend ne suffit pas à l'enregistrer. Le schéma du manifest et celui de la section frontend sont versionnés séparément des composants et des contrats d'interface.

Exemple conceptuel :

```toml
[frontend]
enabled = true
shell_api = "^1.0.0"

[[frontend.contributions]]
type = "ROUTE"
id = "acme.crm.contacts"
entry = "frontend/routes/contacts"
version = "1.0.0"
```

Les permissions d'affichage sont des indications d'interface et ne constituent jamais une autorisation. Toute action sensible doit être refusée ou acceptée par le backend Django selon le `Subject`, la ressource, l'action et le contexte tenant.

## 27. Design System

Le Design System est un contrat frontend public composé de trois niveaux :

```text
Tokens sémantiques
        ↓
Primitives UI accessibles
        ↓
Adapters de rendu
```

Les tokens sémantiques décrivent les intentions de présentation plutôt que des valeurs directement codées dans les modules : couleurs de surface et de contenu, typographie, espacements, dimensions, rayons, élévations, motion et états d'interaction. Une primitive expose une API stable, des variantes déclarées, des états d'accessibilité et des comportements testables. Un adapter traduit ce contrat vers TanStack et le moteur de rendu ou de styles sélectionné.

Le contrat, les tokens et les primitives sont versionnés indépendamment des thèmes et des modules consommateurs. Un module ne doit pas dépendre de la structure CSS privée, d'un sélecteur interne ou d'un composant non public. Il peut composer les primitives et définir des variantes locales dans son périmètre, mais ne doit pas modifier globalement une primitive partagée. Le Design System ne porte aucune règle métier ni autorisation.

Le niveau cible d'accessibilité du shell et des primitives est WCAG 2.2 AA. Une primitive doit documenter sa structure sémantique, son nom accessible, ses rôles et états, son ordre de tabulation, sa gestion du focus, ses messages d'erreur, ses contrastes, son comportement au zoom et son comportement avec la réduction des mouvements. Les composants interactifs doivent fonctionner au clavier et avec les technologies d'assistance. Les éléments HTML natifs sont préférés ; ARIA ne doit pas recréer ou contredire une sémantique native. L'automatisation peut détecter une partie des défauts, mais la validation inclut des parcours manuels au clavier et avec des technologies d'assistance. Une primitive non conforme ne doit pas être publiée comme stable.

Le responsive est mobile-first et fondé sur les contraintes de l'espace de rendu. Une primitive déclare ses dimensions minimales, ses règles de reflow, ses variantes de densité et son comportement lorsqu'une zone devient étroite. Les breakpoints sont des tokens sémantiques de layout ; un adapter peut utiliser des media queries ou container queries sans exposer ce choix comme une dépendance du contrat. Les tableaux doivent proposer une stratégie déclarée pour les petits écrans, par exemple défilement contrôlé, réduction de colonnes ou représentation en cartes. Les formulaires et navigations doivent préserver l'ordre, le focus, la lisibilité et l'accès aux actions à travers les tailles d'affichage. Une extension ne doit pas supposer une largeur, hauteur ou orientation fixe.

Les tokens doivent exprimer une intention sémantique et disposer d'un type, d'une valeur par défaut, de contraintes et, lorsque nécessaire, d'une valeur par mode. Les modes obligatoires sont `light` et `dark`. Un thème `high-contrast` peut ajouter des valeurs destinées à renforcer la perception et la lisibilité, mais il ne peut pas supprimer les garanties minimales des primitives. La résolution suit l'ordre `préférence utilisateur → préférence système → défaut d'installation`. Le shell doit pouvoir appliquer un changement de thème sans recharger la page et exposer le thème courant en lecture seule aux extensions. Un adapter peut matérialiser les tokens en variables CSS, objets de style ou autre mécanisme, mais les identifiants et garanties du contrat restent indépendants de cette représentation.

## 28. Internationalisation

Les locales du frontend utilisent des identifiants Unicode/BCP 47 canoniques. Le shell résout la locale selon l'ordre suivant :

```text
préférence utilisateur
        ↓ sinon
préférence tenant
        ↓ sinon
préférence navigateur
        ↓ sinon
défaut de l'installation
```

Les catalogues sont attachés au composant qui possède le texte et les clés sont namespacées afin d'éviter les collisions. Un module peut fournir plusieurs catalogues et déclarer les locales obligatoires ou optionnelles. Le fallback d'une locale suit une chaîne déterministe, par exemple `fr-CA → fr → locale par défaut`. Le chargement différé est permis, mais une interface ne doit pas présenter une clé brute sans état diagnostiquable.

Les messages dynamiques utilisent un format structuré compatible avec ICU MessageFormat pour les variables, pluriels, sélections et genres. Les nombres, dates, heures et devises doivent être formatés par les données de locale et non par des chaînes codées en dur. La concaténation de phrases ou de fragments traduisibles est interdite. Les messages accessibles, les labels, les descriptions, les erreurs et les annonces de statut passent par le même mécanisme.

La direction d'écriture est dérivée de la locale. Les composants doivent utiliser des propriétés logiques et supporter le passage entre LTR et RTL sans modifier leur logique métier. Une locale obligatoire manquante, une clé dupliquée ou une ressource invalide doit échouer la validation du composant. Un fallback runtime autorisé doit être journalisé dans le diagnostic sans exposer de donnée sensible.

`en` est la locale canonique des catalogues et la racine de fallback du framework. La locale par défaut d'une installation est une configuration, et peut être `fr-FR`, `en-US` ou une autre locale supportée. La présence d'un catalogue canonique `en` ne dispense pas de déclarer les locales obligatoires d'un composant. Les clés, paramètres, catégories grammaticales et structures ICU restent identiques entre les traductions.

Le shell expose un `PresentationContext` distinct du contexte métier :

```text
locale
timezone
calendar
numbering_system
display_currency
```

Chaque dimension possède sa propre résolution et sa propre validation. Le fuseau de présentation suit la préférence utilisateur, puis tenant, puis installation ; l'absence de préférence ne doit pas faire dépendre le contrat de l'horloge locale du navigateur. Les instants persistés et échangés restent en UTC, avec une conversion explicite pour l'affichage. Le calendrier, le système de numération et la devise d'affichage ne changent pas le calendrier métier, la précision des montants, la devise comptable ou les calculs d'échéance. Une extension consomme ce contexte en lecture seule et ne peut pas l'utiliser pour contourner une règle backend.

## 29. Observabilité, sécurité et diagnostic

Pixs distingue trois catégories :

```text
Observabilité technique  logs, métriques et traces d'exécution
Audit fonctionnel        événements persistants d'actions métier ou de sécurité
Diagnostic opérateur     état, composition, santé et raisons d'échec
```

Les signaux techniques utilisent un modèle compatible OpenTelemetry sans imposer de collecteur ou de backend concret. Les signaux HTTP, Commands, Queries, Events, Jobs, notifications et webhooks doivent propager le contexte lorsqu'ils restent dans un même parcours d'exécution. La propagation inter-composants utilise W3C Trace Context lorsque le transport le permet. Un contexte peut contenir :

```text
trace_id
span_id
parent_span_id éventuel
correlation_id
causation_id éventuel
component_id
component_version
operation
tenant_id lorsque nécessaire et autorisé
subject_reference pseudonymisée lorsque nécessaire et autorisée
```

`trace_id` et `span_id` identifient le parcours technique ; `correlation_id` identifie le parcours applicatif et peut survivre à plusieurs traitements asynchrones ; `causation_id` relie une exécution à l'événement ou à la Command qui l'a provoquée. Aucun de ces identifiants ne remplace l'identité numérique, le contexte tenant ou une preuve d'autorisation.

Les logs sont structurés, horodatés en UTC, associés au composant et à l'opération et classés par niveau. Ils ne doivent pas contenir par défaut de payload complet, token, secret, mot de passe, clé privée, données d'authentification ou contenu personnel non nécessaire. Les logs peuvent contenir une référence technique redacted ou pseudonymisée lorsque le diagnostic le justifie. Les valeurs contrôlées par un utilisateur doivent être bornées et encodées afin de ne pas falsifier la structure du journal.

Les métriques utilisent des noms et unités stables ainsi que des labels à cardinalité bornée. Les identifiants utilisateur, tenant, requête ou ressource ne doivent pas devenir des labels métriques par défaut. Les traces peuvent contenir des attributs supplémentaires soumis aux mêmes règles de minimisation, redaction et contrôle d'accès que les logs.

L'audit fonctionnel est séparé des logs techniques. Un événement d'audit doit pouvoir représenter au minimum :

```text
audit_id
occurred_at
subject ou actor_reference
tenant_id lorsque pertinent
action
resource_type
resource_id
outcome
reason ou error_code éventuel
correlation_id
causation_id éventuel
component_id et component_version
```

L'audit des authentifications, changements d'identité, autorisations sensibles, accès inter-tenants, mutations métier significatives, modifications de configuration et opérations destructives doit être persistant, contrôlé et soumis à une politique de rétention. Les valeurs avant/après sont limitées aux champs nécessaires, redacted lorsqu'elles sont sensibles et ne doivent pas transformer l'audit en copie de la base métier.

Le diagnostic est une capacité de lecture destinée à l'exploitation et au support autorisé. Il peut exposer l'identité et la version du composant, son lifecycle, ses dépendances résolues, ses contrats et versions, ses capacités, ses limites, ses derniers états de santé, ses compteurs d'erreur et les raisons d'un état `DEGRADED`, `FAILED` ou `DISABLED`. Il ne doit pas exposer de secret, de token, de payload sensible, de requête complète ou de commande destructive. Les actions de diagnostic doivent être sans effet métier par défaut ; toute action de réparation ou de reconfiguration passe par une opération explicitement autorisée et auditée.

Les probes runtime sont séparées :

```text
liveness   processus capable de répondre
startup    initialisation et composition terminées
readiness  traitement du trafic autorisé
diagnostic état détaillé réservé à l'exploitation
```

`liveness` ne doit pas échouer uniquement parce qu'une dépendance métier est indisponible. `startup` ne devient positif qu'après validation des préconditions nécessaires, de la composition et des migrations autorisées. `readiness` vérifie les dépendances obligatoires, les contrats actifs, la configuration effective et les ressources indispensables au trafic. Une dépendance optionnelle absente peut laisser la capacité en `DEGRADED` si ses limites sont explicites ; elle ne doit pas masquer une défaillance de sécurité ou d'isolation. Les probes doivent avoir un délai et un coût bornés, ne pas modifier l'état métier et produire des signaux corrélables sans contenu sensible. Les endpoints ou rapports détaillés de diagnostic doivent exiger l'identité, le tenant et les permissions adaptés.

La redaction est appliquée à la frontière de production des signaux, et non uniquement lors de leur exportation. Chaque composant doit pouvoir déclarer les champs sensibles de ses événements et erreurs. Une collecte indisponible ne doit pas bloquer une mutation métier conforme, mais la perte de télémétrie doit être signalée par un état ou une métrique technique. Les échantillonnages, seuils, rétentions et destinations sont configurables sans modifier la sémantique des contrats métier.

La rétention et l'accès sont définis par catégorie de signal :

```text
logs        données techniques à durée courte ou contrôlée
métriques   agrégats à conservation configurable
traces      échantillons détaillés à rétention limitée
audit       événements fonctionnels persistants et append-only
diagnostic  état courant et historique technique limité
```

Chaque politique déclare la durée, la portée tenant, les rôles autorisés, les conditions de pseudonymisation, les règles d'export et le comportement en cas de legal hold. Les logs, métriques et traces ne doivent pas conserver une identité, un tenant ou un payload lorsqu'une agrégation ou une référence pseudonymisée suffit. Les diagnostics tenant-scoped ne sont visibles que dans le contexte autorisé ; un accès plateforme ou inter-tenant doit être explicitement autorisé, corrélé et audité.

L'audit est append-only dans son usage normal. Lorsqu'une obligation de suppression ou de minimisation s'applique, le système doit utiliser une procédure explicite et auditable d'anonymisation ou de purge de champs autorisés, sans présenter une réécriture silencieuse comme un événement nouveau. L'expiration des données techniques est automatique lorsque la politique le permet. Une collecte ou une rétention indisponible est diagnostiquée, mais ne doit pas créer une autorisation ou bloquer une mutation métier conforme.

Chaque composant possède un profil de sécurité déclaratif comprenant au minimum :

```text
data_classes       classes de données manipulées
permissions        permissions requises
secret_references  secrets consommés par référence
network_boundaries entrées, sorties et dépendances réseau
dependencies       dépendances runtime et build
trust_level        niveau de confiance attendu
security_controls  contrôles requis ou fournis
```

Le profil ne doit pas contenir de valeur secrète. Il permet de vérifier qu'un composant ne demande pas une permission, un secret ou une sortie réseau non déclarés. Les dépendances doivent être inventoriées dans un SBOM et soumises à une politique de vulnérabilité. Les artefacts doivent être associés à une provenance vérifiable, une empreinte et, lorsque la distribution l'exige, une signature. La vérification de l'artefact doit pouvoir confirmer la source, la version, le processus de build et les entrées principales.

Le socle de build couvre le scan de secrets, l'analyse statique, la vérification des dépendances et de leurs vulnérabilités, le scan des images ou paquets, la génération du SBOM, la vérification des signatures et le contrôle de provenance. Une vulnérabilité critique connue bloque la distribution. Une vulnérabilité élevée peut uniquement faire l'objet d'une dérogation explicite avec justification, responsable, échéance, mesures compensatoires et audit. Les résultats de sécurité sont diagnostiquables sans exposer les détails exploitables ou les données sensibles.

Les contrôles de sécurité utilisent une politique fail-closed pour les décisions d'identité, d'autorisation, de signature, de secret, de contexte tenant, d'intégrité d'artefact et de validation de provider. Une information absente, expirée, incohérente ou indémontrable ne doit pas être interprétée comme un accord. Une capacité optionnelle peut passer à `DEGRADED` ou `DISABLED` si son isolement ne permet aucun accès ou traitement non autorisé. Le runtime doit pouvoir révoquer un composant, un provider, un token, une clé de webhook ou un endpoint sans supprimer implicitement les données métier. Les transitions de blocage, révocation, dérogation et réactivation portent une cause, une corrélation, un acteur autorisé et un événement d'audit ; le diagnostic expose l'état et la référence sans publier le secret ou le détail exploitable.

La politique fail-closed s'applique également à un niveau d'assurance absent, expiré, non mappé ou inférieur au niveau requis. Un échec de vérification ou de step-up ne doit jamais être converti en assurance inférieure acceptée pour une action sensible. Les diagnostics peuvent exposer le niveau et la cause du refus, mais jamais le token, la preuve ou le credential.

Les décisions d'autorisation sensibles, les changements de politiques, de rôles, d'ACL, de memberships, de scopes, les révocations, les step-up et les élévations contrôlées doivent produire un audit corrélable. Les autorisations courantes ne doivent pas nécessairement journaliser chaque succès ; les refus et événements de sécurité doivent rester observables sans exposer les attributs, payloads ou politiques confidentiels.

Un avis de sécurité public ou interne doit identifier le composant, la version ou plage de versions affectée, la sévérité, la surface concernée, l'impact, la correction, la mitigation, le statut de révocation et les conditions de retour à un état sûr. Les avis et décisions de sécurité sont eux-mêmes versionnés et auditables. L'installation, le démarrage et la mise à niveau doivent vérifier les révocations et pouvoir refuser un artefact ou une composition compromise. Une procédure d'urgence peut suspendre, désactiver ou remplacer un composant sans attendre une évolution fonctionnelle ordinaire, mais elle ne doit pas contourner l'audit, l'autorisation ni les migrations nécessaires.

Un `SecurityIncident` doit pouvoir relier un avis, une timeline, les composants et versions impliqués, les signaux corrélés, les décisions, les mesures de confinement, les notifications et la récupération. Les preuves techniques sont minimisées, protégées et rétentées selon la politique applicable. La récupération doit privilégier l'isolement, la révocation, la restauration vérifiée et la reprise progressive ; elle ne doit pas purger automatiquement les données métier. Les tests de reprise doivent pouvoir être exécutés sans reproduire un secret ou exposer une donnée de production.

## 30. Stockage objet et fichiers

Le stockage binaire est exposé par un contrat public `ObjectStorageProvider`. Il sépare les octets, les métadonnées Pixs, les relations métier et les règles d'autorisation. Le contrat ne doit imposer ni fournisseur, ni protocole, ni topologie de déploiement.

Un objet de fichier Pixs possède conceptuellement au minimum :

```text
file_id                 UUIDv7 stable
tenant_id               lorsque l'objet est tenant-scoped
owner_reference         sujet ou module propriétaire
name                    nom d'affichage contrôlé
media_type              type déclaré et type détecté éventuel
size                    taille validée
checksum                empreinte du contenu
provider_id             provider objet sélectionné
object_reference        référence opaque du provider
version                 version métier ou technique
state                   état du cycle de vie
retention_policy        politique de conservation éventuelle
```

PostgreSQL reste la source de vérité des métadonnées, relations, permissions, états, mappings et opérations Pixs. Le provider conserve les octets et doit pouvoir vérifier leur taille et leur checksum. Les identifiants, chemins internes et URLs du provider ne constituent pas des identifiants métier Pixs.

Les providers de référence peuvent être un filesystem local pour le développement et les tests, ainsi que des implémentations S3-compatible comme S3, MinIO ou Ceph Object Gateway. Un provider peut proposer la création réservée, l'upload direct ou multipart, la reprise, la finalisation, la lecture contrôlée, une URL temporaire, le contrôle d'intégrité, la suppression différée et la récupération d'état.

Les états de référence sont :

```text
PENDING
UPLOADING
QUARANTINED
AVAILABLE
FAILED
DELETED
EXPIRED
```

Un objet finalisé est immuable par défaut. Un remplacement crée une nouvelle version ou un nouvel objet relié explicitement à la ressource métier. La suppression logique, l'expiration, la purge physique et la récupération sont distinctes, soumises aux permissions, à la rétention, aux éventuels legal holds et à l'audit. Les objets orphelins et les divergences entre métadonnées et provider doivent être détectables et réparables par une opération explicite.

La métadonnée Pixs est l'autorité de l'état de cycle de vie de l'objet. Un tombstone doit être conservé et propagé avant une reconstruction ou une reprise qui pourrait republier l'objet. La durée de rétention des octets peut différer de celle de la métadonnée, mais cette différence doit être déclarée et ne doit pas permettre la résurrection d'une référence supprimée.

Les fichiers sont privés par défaut. L'accès passe par une API autorisée ou par une URL temporaire générée après résolution de l'identité numérique, du tenant et des permissions. Les secrets du provider sont référencés par le système de secrets et ne doivent apparaître ni dans les métadonnées, ni les logs, ni les traces, ni les URLs générées. Une opération longue ou externe passe par un `Command` ou un `Job` et ne rend pas le fichier disponible avant la finalisation et les validations nécessaires.

## 31. Référentiels documentaires et Nextcloud

Un référentiel documentaire collaboratif est exposé par un contrat distinct, `DocumentRepositoryProvider`. Il ne doit pas être confondu avec `ObjectStorageProvider` : il porte des documents, dossiers, versions, partages, verrous et modifications externes selon les garanties du système intégré.

L'adapter Nextcloud peut connecter une instance locale ou distante au moyen d'une configuration d'endpoint et de credentials gérés par le système de secrets. Il utilise ses interfaces publiques, notamment WebDAV, OCS ou les APIs appropriées, valide la connexion et n'accède jamais directement au répertoire interne de données ou au bucket primaire de Nextcloud.

Nextcloud peut être utilisé comme :

```text
référentiel documentaire piloté dans Pixs
    Pixs porte le modèle métier et l'autorité applicative ;
    Nextcloud fournit la conservation ou la présentation documentaire ;
    les écritures passent par Pixs et son autorisation.

référentiel documentaire externe
    Nextcloud peut être modifié indépendamment ;
    Pixs conserve une projection, les mappings et l'état de synchronisation.
```

Si Nextcloud utilise un stockage objet S3-compatible comme stockage primaire, ce bucket est considéré comme exclusivement géré par Nextcloud. Pixs ne doit pas y accéder directement. Une même infrastructure objet peut être utilisée avec des buckets, credentials et espaces séparés. Les références Nextcloud, identifiants externes, versions et `ETag` restent distincts des `file_id` et versions Pixs.

Dans le mode piloté par Pixs, une écriture documentaire est initiée par une Command autorisée et le référentiel externe est une dépendance de conservation ou de présentation. Une modification externe inattendue devient une divergence diagnostiquable et ne remplace pas silencieusement l'état Pixs. Dans le mode externe, les modifications distantes sont normales ; elles sont importées selon le mapping, le contexte tenant, la politique d'autorité et la stratégie de conflit déclarés.

Le mode, la source d'autorité, le sens de synchronisation, la stratégie de conflit et les règles de suppression sont déclarés par espace documentaire ou capacité. Une modification externe ne devient pas automatiquement une mutation métier acceptée : elle est vérifiée, rattachée à une identité ou un provider, dédupliquée, autorisée lorsque nécessaire, puis transformée en Command ou événement interne versionné.

## 32. Recherche et projections

La recherche est exposée par un contrat public `SearchProvider`. Elle repose sur des projections reconstrusibles et ne constitue jamais la source de vérité métier. PostgreSQL ou le référentiel propriétaire reste l'autorité ; l'index est un artefact dérivé, versionné et supprimable/reconstructible.

Le provider actif est résolu explicitement et déterministiquement selon les capacités déclarées. Le contrat ne dépend pas d'un moteur particulier, d'un format d'index ou d'un algorithme de pertinence. Plusieurs providers de recherche nécessitent une composition déclarée, par exemple une fédération ou un routeur, et ne peuvent pas être sélectionnés selon l'ordre de découverte.

Le contrat peut couvrir :

```text
full_text
structured_filters
facets
sorting
cursor_pagination
autocomplete
locale_aware_analysis
semantic_search optionnelle
```

Les champs filtrables, triables et recherchables sont déclarés par la ressource. Les requêtes ne peuvent pas fournir de fragment SQL, ORM, expression d'index ou champ non déclaré. Le tri, le curseur, le score et les limites doivent être documentés par le contrat API.

Les index doivent intégrer ou vérifier le contexte de sécurité : tenant, identité numérique, ACL, état de publication, expiration et suppression. Une modification d'autorisation doit pouvoir invalider ou mettre à jour les documents concernés. Une défense en profondeur peut filtrer à nouveau lors de la requête, mais l'index ne doit pas être considéré comme une frontière d'autorisation suffisante à lui seul.

La construction ou la mise à jour d'une projection est déclenchée par des événements, des Jobs ou une commande de reconstruction. Elle suit une garantie au moins une fois et doit être idempotente. Un retard d'indexation doit être observable ; l'état `STALE`, une fenêtre de fraîcheur ou une cohérence éventuelle doivent être déclarés. Une panne de recherche peut produire un mode dégradé lorsque la recherche n'est pas une dépendance obligatoire de la mutation ou de l'autorisation.

Une Query de recherche est soumise aux mêmes validations d'identité, de tenant, d'ACL, de pagination, de limitation de débit et de redaction qu'une Query classique. Le score, le classement et la fraîcheur sont des propriétés du contrat de recherche ; ils ne doivent pas être interprétés comme une décision d'autorisation ou comme une preuve de complétude des données.

## 33. Workflows

Le runtime de workflow fournit une capacité générique et versionnée, sans posséder les invariants propres aux modules métier. Une définition peut contenir des états, transitions, gardes, actions, délais, événements, annulations et conditions de reprise.

Les définitions publiées et les instances actives sont persistantes dans PostgreSQL ou dans le provider de persistance autoritatif déclaré par Pixs. L'état courant, la version interprétée, le sujet, le contexte tenant, les références métier et l'historique nécessaire à la reprise ne doivent pas dépendre de la mémoire d'un worker ou d'un fichier local éphémère.

```text
WorkflowDefinition
    definition_id
    definition_version
    states
    transitions
    guards
    actions
    timers

WorkflowInstance
    instance_id
    definition_version
    subject
    tenant_context
    current_state
    context_reference
    pending_actions
    history_reference
```

Une transition est une Command soumise à l'identité numérique, au tenant, aux permissions et aux invariants du module propriétaire. La transition et la mise à jour de l'état du workflow doivent respecter une frontière transactionnelle explicite. Les effets asynchrones utilisent l'outbox et les Jobs ; ils ne doivent pas rendre la transition acquise avant que la garantie déclarée ne soit satisfaite.

Les états, transitions et gardes doivent être déterministes à définition, contexte et entrée identiques. Les actions exécutables sont des handlers déclarés par des capacités ou contrats publics ; une définition de workflow ne peut pas charger un module arbitraire, exécuter une expression non contrôlée ou recevoir un accès implicite à une ressource d'un autre module.

Les workflows longs doivent prévoir la reprise, les retries, les timeouts, l'annulation, l'intervention manuelle, la compensation éventuelle et la dead-letter. Les handlers sont idempotents ou déclarent leurs limites. Une définition ne doit pas permettre l'exécution arbitraire de code, l'accès implicite à un module ou le contournement d'une ACL.

Les versions de définition restent disponibles pour les instances en cours selon une politique déclarée. Une migration de workflow est distincte d'une migration de données métier et doit être versionnée, testée, autorisée et auditée. Les transitions significatives, erreurs, délais, actions manuelles et changements de définition produisent des événements d'audit adaptés.

## 34. Synchronisations externes

Une synchronisation est exposée par un contrat `SynchronizationProvider` et par un moteur d'orchestration générique. Le provider traduit les API, événements et identifiants d'un système externe ; le moteur gère les mappings, checkpoints, retries, conflits, audit et diagnostic.

Chaque synchronisation déclare :

```text
resource_type
mode                 IMPORT | EXPORT | BIDIRECTIONAL | PROJECTION
source_of_truth
authority_mode       PIXS | EXTERNAL | EXPLICIT_BIDIRECTIONAL
direction
external_scope
mapping_version
trigger              webhook | polling | schedule | command
conflict_strategy
deletion_policy
consistency_target
```

Les identifiants externes sont stockés dans une table ou ressource de mapping unique selon le provider, le compte externe, le tenant et la ressource. Ils ne remplacent jamais les identifiants internes. Les cursors, checkpoints, `ETag`, versions externes, timestamps de dernière observation, états de convergence et empreintes de payload sont persistants lorsque nécessaires à la reprise ou à l'idempotence.

Les modes d'exécution suivent `at-least-once`. Les messages peuvent être rejoués et les handlers doivent être idempotents. Les échecs passent par un backoff, une limite de tentatives, une dead-letter et une action de reprise explicite. Les quotas et limites du provider sont respectés. Aucune synchronisation ne suppose une transaction distribuée ou une garantie `exactly-once` de bout en bout.

Les conflits sont explicitement traités par une stratégie déclarée, par exemple `REJECT`, `MANUAL_REVIEW`, `LAST_WRITE_WINS`, `SOURCE_PRIORITY` ou `DOMAIN_MERGE`. `LAST_WRITE_WINS` n'est autorisé que pour une ressource dont la perte d'une modification concurrente est acceptable. Une modification ou suppression distante ne doit jamais écraser silencieusement une donnée Pixs autoritative.

Pixs est la source d'autorité par défaut pour ses données métier. `PIXS` signifie que les mutations autoritatives sont décidées par Pixs et que l'externe est une destination, une copie ou une projection. `EXTERNAL` signifie que le référentiel distant peut décider de l'état de la ressource et que Pixs en conserve une projection contrôlée. `EXPLICIT_BIDIRECTIONAL` est réservé aux ressources dont la convergence et la perte potentielle d'une modification sont spécifiées ; il exige une stratégie de conflit et de suppression explicite. Une valeur absente ou ambiguë ne doit jamais être interprétée comme une double autorité permissive.

Un référentiel externe peut être autoritatif pour un espace documentaire déclaré. Une double autorité n'est jamais implicite ; elle doit disposer d'une stratégie de convergence et de conflit propre à la ressource. Toute modification importée qui affecte un invariant métier passe par une Command, une autorisation, une idempotence et un audit.

Le provider et la configuration de synchronisation sont résolus explicitement et déterministiquement. Une synchronisation possède un état opérationnel distinct de l'état des données :

```text
PENDING
RUNNING
PAUSED
DEGRADED
FAILED
CONVERGED
QUARANTINED
```

La suspension, la reprise, la réinitialisation du checkpoint, la résolution manuelle d'un conflit et la sortie de quarantaine sont des opérations autorisées et auditées. Une réinitialisation ne doit pas entraîner une suppression ou une duplication non maîtrisée ; elle doit préciser le périmètre, le curseur de départ et la stratégie de rejeu.

Les credentials, scopes, endpoints, certificats, clés de signature et limites du provider sont configurés par référence au système de secrets et ne doivent pas être déduits d'un payload externe. Les webhooks entrants vérifient la signature, la fenêtre de rejeu, l'identifiant externe et l'empreinte du message avant de créer une Command ou un événement interne. Les appels sortants utilisent l'outbox, des retries bornés et une dead-letter. Les événements et erreurs de synchronisation propagent les corrélations, le tenant et le provider sans exposer de secret ou de payload inutile.

### 34.1 Projection LDAP des primitives Core

Un `DirectoryProjectionProvider` peut projeter en lecture les identités
numériques, groupes et appartenances de `pixs.core` vers LDAP. Il est toujours
configuré avec `authority_mode` `PIXS` et une direction sortante ; LDAP n'est
ni une source de mutation, ni un moteur d'autorisation, ni un provider
d'authentification par effet de cette projection. Les ACL, permissions,
mécanismes de révocation et décisions ne sont pas délégués à LDAP.

Le provider déclare le mapping versionné, l'allowlist d'attributs, les tenants
et scopes, les limites de fraîcheur et la politique de suppression. Les
identifiants canoniques Pixs restent stables ; le DN LDAP et les identifiants
externes sont des mappings persistants du provider. Les données non classifiées
ou hors périmètre ne sont pas exportées.

La façade de consultation de `pixs.core` reste l'unique point d'accès des
consommateurs. Elle vérifie l'autorisation et le `ScopeContext`, lit LDAP
seulement lorsque le provider déclaré est disponible et convergé dans la limite
de fraîcheur, puis lit PostgreSQL en cas d'indisponibilité ou de retard. Après
une mutation confirmée, elle privilégie PostgreSQL jusqu'à confirmation de la
projection. Le repli produit un état `DEGRADED` corrélé ; il ne peut ni exposer
une donnée hors périmètre ni élargir une autorisation.

## 35. Conformité des providers et capacités du point 12

Les contrats `ObjectStorageProvider`, `DocumentRepositoryProvider`, `SearchProvider` et `SynchronizationProvider` doivent disposer d'une suite de conformité versionnée. Cette suite vérifie les garanties du contrat, indépendamment de la technologie du provider. Le runtime ne doit pas déclarer compatible un provider dont la conformité obligatoire est absente, expirée ou échouée.

Les providers de persistance, stockage, recherche, synchronisation et référentiels documentaires doivent préserver les invariants de scope : propagation du `ScopeContext`, propriété canonique, cohérence `tenant_id`/`scope_id`, absence de fuite entre tenants ou scopes et refus des accès hors périmètre. Les tests doivent être exécutables avec la topologie PostgreSQL de référence et avec toute topologie isolée déclarée compatible. Une différence de topologie ne peut pas modifier silencieusement les règles d'autorisation, de partage, de projection ou de suppression.

La conformité couvre au minimum :

```text
contrat et version
capacités déclarées
tenant et autorisation
identifiants et mappings
états et lifecycle
idempotence et rejeu
reprise et interruption
erreurs et limites
audit et observabilité
secrets et scopes
```

Les tests doivent distinguer les garanties obligatoires des capacités optionnelles. Une capacité optionnelle absente ou indisponible peut produire `DEGRADED` ou `DISABLED` si elle reste isolée et si aucune mutation, autorisation ou donnée n'est implicitement perdue. Une incompatibilité de contrat, une ambiguïté de provider, un défaut d'isolation tenant ou une violation de sécurité bloque l'activation.

## 36. Packaging, upgrade et exploitation

`BUILD.md` définit intégralement la construction, le packaging, le déploiement,
les mises à niveau et l'exploitation des artefacts Pixs. Les garanties
normatives associées sont portées par les capacités OpenSpec concernées.
Ce document ne duplique pas leurs modalités techniques.

## 37. Sauvegarde et reprise après sinistre

Les détails de sauvegarde, de restauration, de reprise et de publication sont
définis dans `BUILD.md`, en cohérence avec les capacités OpenSpec de cycle de
vie, de sauvegarde, de compatibilité et de release.

## 38. Interface d'exploitation

L'interface d'exploitation, les opérations de management et l'état
`MAINTENANCE` sont définis dans `BUILD.md` et par la capacité OpenSpec
`operations`. Ils restent distincts de l'API métier.

## 39. Providers concrets et modules métier

Les providers et modules métier sont des `Component` versionnés. Leur manifest doit déclarer leurs capacités fournies et requises, contrats implémentés, dépendances, configuration, compatibilité, lifecycle, niveau de confiance et tests de conformité applicables.

Les niveaux de confiance sont :

```text
PLATFORM     composant maintenu dans l'écosystème Pixs
TRUSTED      composant tiers signé, vérifié et autorisé par contrat public
SANDBOXED    contribution isolée avec APIs et permissions limitées
DEVELOPMENT  composant réservé au développement local
```

Le niveau de confiance est distinct du type de composant et ne doit pas
masquer une implémentation métier ou un provider concret. Un composant
`PLATFORM` reste soumis à son versionnement, lifecycle, configuration,
signature et sélection. Un composant `DEVELOPMENT` ne peut pas être utilisé en
production ; un composant `SANDBOXED` n'accède qu'aux APIs et permissions
explicitement accordées. Les composants `TRUSTED` et `SANDBOXED` doivent
respecter les contrats publics et garanties de sécurité qu'ils déclarent.

Le resolver ne doit jamais activer automatiquement un provider parce qu'il est présent sur le filesystem, importable ou livré dans l'image. La résolution suit la configuration explicite, puis un candidat compatible unique ; plusieurs candidats ou l'absence d'un provider requis produisent une composition invalide. Un fallback concret doit être déclaré comme une composition ou une politique de capacité et ne peut pas être déduit silencieusement.

`pixs.core` fournit les primitives transverses — identité, tenant, autorisation, configuration, lifecycle, contrats et persistance commune — sans porter les invariants d'un domaine métier particulier. Un module métier possède ses modèles, migrations, permissions, Commands, Queries, Events et invariants. Un autre module ne peut pas écrire directement ses tables ou importer son implémentation privée ; il utilise ses interfaces publiques.

Un module métier peut requérir un provider ou une capacité concrète, mais cette dépendance doit être déclarée, versionnée et justifiée. Les providers d'intégration externe restent des adapters : ils traduisent un protocole ou un service sans déplacer automatiquement la source de vérité métier hors de Pixs.

## 40. Capacités d'extension de plateforme

### 40.1 Registres et fournisseurs de composants

Un `ComponentRegistryProvider` peut fournir un catalogue, la recherche, la
résolution d'une version, la récupération, l'installation, la révocation et le
retrait de composants signés. Il ne remplace pas le résolveur local, ne choisit
pas un composant implicitement et commence par les sources privées ou hors ligne
déclarées. Un marketplace public reste un adapter optionnel. La provenance, la
signature, le SBOM, la compatibilité et le niveau de confiance sont vérifiés
avant installation ou activation.

### 40.2 Règles, IA et collaboration

Un `BusinessRuleProvider` évalue un DSL déclaratif restreint, versionné,
testable et audité. Il ne peut pas évaluer du code arbitraire au runtime et est
séparé du PDP d'autorisation et du moteur de workflow ; une règle ne peut pas
accorder un droit sans contrôle d'autorisation.

Les fournisseurs IA et agents sont désactivés par défaut et déclarent leurs
capacités de modèle, outils, mémoire et récupération. Les prompts, évaluations,
budgets, appels et usages de données sont versionnés, gouvernés et audités. Les
outils exécutés par un agent passent par des Commands ou contrats autorisés ;
un fournisseur de modèle ne reçoit que les données que le `ScopeContext`, la
gouvernance, la finalité et une politique stricte de sortie autorisent.

La collaboration temps réel utilise un contrat distinct de la synchronisation
de projections. Une session collaborative porte son périmètre, ses participants,
ses droits, ses opérations et son état de convergence. CRDT et OT sont des
adapters possibles, sans référence retenue avant l'identification des premières
ressources collaboratives ; ils ne valident jamais seuls une mutation métier.

### 40.3 Caches, analytique et clients natifs

Un `CacheProvider` peut conserver des données dérivées uniquement. Ses clés,
tags et invalidations incluent le tenant, le scope, l'identité lorsque requis,
la version et la classification. Les protections contre stampede, les TTL, les
états de fraîcheur et l'échec dégradé restent déclarés ; aucune lecture de cache
ne contourne l'autorisation ni ne devient une source de vérité.

Les projections analytiques, la couche sémantique et les rapports sont des
composants propriétaires de leurs dérivés. Leurs requêtes et exports passent
par un filtrage autorisé à la source et conservent la résidence, la rétention,
la minimisation et la lignée de la donnée.

Les SDK de clients natifs gardent une séparation entre transport, stockage
sécurisé local et intégrations de plateforme. Les notifications push, liens
profonds et informations d'appareil sont des adapters explicitement déclarés ;
aucun credential de session n'est exposé à un stockage non sécurisé.

### 40.4 Secrets, SCIM, déploiement et preuves d'audit

Un `SecretProvider` ne retourne des secrets qu'au runtime selon une référence,
une identité de workload et une politique déclarée. Il privilégie des
credentials courts et fournit rotation, révocation, durée de vie, audit et
erreurs non divulguantes. Le contenu d'un secret ne peut pas être journalisé,
sérialisé dans un rapport ou incorporé à un artefact.

Un provider SCIM traduit le provisionnement externe vers les Commands de
`pixs.core`, avec signature ou authentification du fournisseur, idempotence,
mapping explicite, désactivation contrôlée et audit. Il ne crée aucune relation
d'autorisation implicite.

Le déploiement progressif coordonne des révisions compatibles à partir de
health gates et de métriques déclarées. Il ne contourne ni les migrations, ni
les validations de release, ni les politiques de feature flags. Les preuves
d'intégrité d'audit utilisent d'abord un chaînage vérifiable et peuvent ajouter
un scellement externe ; un stockage WORM reste une politique de déploiement
optionnelle. Elles sont vérifiables, versionnées et ne rendent pas les données
personnelles ou les secrets immuables au-delà de leur régime légal.

## 41. Runtime de référence, P0 et objectifs de service

Le runtime de référence est Django, PostgreSQL et TanStack. Les contrats du
Kernel préservent l'extensibilité des domaines, providers et intégrations, mais
aucune abstraction multi-runtime ne fait partie du P0. Un adapter de runtime
futur doit être spécifié, versionné et validé sans modifier implicitement les
garanties du runtime de référence.

Le profil P0 impose les capacités de composition, `pixs.core`, contexte de
périmètre, autorisation, API, migrations, runtime, provisionnement, sécurité,
secrets, audit, observabilité, gouvernance, cycle de vie des données et tests
de conformité. Une capacité non P0 doit déclarer son absence ou son état
`DISABLED` sans affaiblir ce socle.

Une décision d'architecture contient son identifiant, son état, son contexte,
les alternatives considérées, ses conséquences, ses spécifications affectées
et sa date de réévaluation éventuelle. Les objectifs de service sont déclarés
par release ou profil : disponibilité, latence, fraîcheur d'invalidation,
reprise et compatibilité. Leurs seuils sont explicites, versionnés et vérifiés ;
aucun seuil universel n'est déduit du runtime.
