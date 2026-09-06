# TECHNICAL.md — Pixs

Ce document précise les décisions techniques transverses du projet. Il complète `PROJECT.md` sans remplacer les spécifications OpenSpec, qui définiront les comportements implémentables.

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

## 4. Exigences techniques à spécifier

Les futures spécifications OpenSpec devront notamment définir :

* les identifiants internes stables des utilisateurs et identités numériques ;
* les contraintes d'unicité du lien utilisateur-identité ;
* la représentation des comptes de service ;
* les sessions, tokens et méthodes d'authentification ;
* la révocation immédiate ou différée ;
* le provisionnement et le déprovisionnement fédérés ;
* le mapping des identifiants externes ;
* l'audit des authentifications et changements d'état ;
* les règles d'autorisation applicables aux identités sans utilisateur ;
* les règles de migration depuis une éventuelle représentation utilisateur historique.

Ces exigences ne doivent pas introduire de relation plusieurs-à-plusieurs entre utilisateurs et identités numériques sans décision architecturale explicite.

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

## 9. Versionnement des contrats

Les contrats publics utilisent SemVer 2.0.0 indépendamment de la version du composant qui les implémente.

```text
component_version
contract_version
capability_version
manifest_schema_version
```

Ces versions peuvent évoluer séparément. Une correction interne compatible peut modifier la version du composant sans modifier la version du contrat.

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

## 11. Multi-tenancy

`Tenant` est la frontière technique d'isolation des données et du contexte d'autorisation. `Organization` peut représenter une entité métier, mais ne constitue pas nécessairement une frontière technique.

Le modèle doit supporter :

```text
DigitalIdentity N ─── N Tenant
          via TenantMembership
```

Une appartenance doit être explicitement représentée, activable, révocable et contextualisée. Une identité numérique peut appartenir à plusieurs tenants. Les comptes de service suivent le même modèle d'appartenance, sans nécessiter d'utilisateur humain.

Pixs doit supporter le mode mono-tenant et le mode multi-tenant. Le mode mono-tenant ne supprime pas les invariants tenant-scoped ; il utilise un tenant courant unique ou un contexte équivalent explicitement configuré.

Les groupes sont tenant-scoped par défaut. Les groupes globaux sont réservés aux besoins de plateforme et leur utilisation dans un tenant doit être explicitement déclarée.

## 12. Autorisation et contexte

L'évaluation d'une autorisation utilise les éléments suivants :

```text
Subject  → identité numérique, utilisateur ou groupe
Resource → ressource protégée
Action   → opération demandée
Context  → tenant courant et autres contraintes applicables
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

Toute ressource tenant-scoped doit être évaluée avec un contexte tenant valide. Les accès plateforme et inter-tenants nécessitent une permission explicite, un contexte d'accès explicite et un événement d'audit. Ils ne constituent jamais un bypass silencieux des ACL.

Le backend Django est l'autorité d'évaluation. Le frontend, les caches, les projections et Electric peuvent refléter une décision mais ne peuvent pas l'autoriser à la place du backend.

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
tenant_id   UUIDv7 du tenant propriétaire si la ressource est tenant-scoped
```

Les horodatages doivent être générés et interprétés en UTC. Le champ `version` permet de détecter les mises à jour concurrentes sans faire de la dernière écriture une résolution implicite.

Le `soft delete` n'est pas une obligation globale du framework. Le module propriétaire doit déclarer la stratégie applicable : suppression physique, marqueur de suppression, archivage ou conservation définitive. Toute suppression doit respecter les références inter-modules, les obligations d'audit et les règles de rétention.

Une entité tenant-scoped doit posséder une référence explicite vers son tenant propriétaire. Le contexte tenant d'une requête ne doit pas être déduit uniquement d'un identifiant fourni par le client.

## 15. Exécution des Commands

Une Command est synchrone par défaut. Le mode asynchrone doit être déclaré explicitement dans le contrat public de la Command.

Une Command publique doit pouvoir transporter :

```text
command_id
command_type
command_version
subject
tenant_context
payload
correlation_id
causation_id
idempotency_key éventuelle
```

Le dispatcher doit valider le type, la version, l'identité appelante, le contexte tenant, le payload et l'autorisation avant d'appeler le handler métier. Le handler exécute la mutation dans la frontière transactionnelle définie par le module propriétaire.

Une Command synchrone retourne un résultat ou une erreur métier après décision de la transaction. Une Command asynchrone retourne un identifiant de suivi et ne doit pas présenter la mutation comme acquise avant l'exécution et la validation correspondantes.

Les identifiants de corrélation et de causalité servent au suivi technique et fonctionnel. Ils ne remplacent pas l'identité numérique, le contexte tenant ou la clé d'idempotence.

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

## 19. Queries

Une Query est une opération de lecture autorisée. Elle doit vérifier l'identité ou le sujet appelant, le contexte tenant et les permissions applicables avant de retourner une projection ou un résultat.

Une Query ne doit pas modifier l'état métier, publier un événement métier, créer implicitement une ressource, modifier un compteur fonctionnel, déclencher une migration ou contourner une ACL. Les caches, métriques et traces sont des effets techniques autorisés lorsqu'ils ne deviennent pas une source de vérité métier.

Une Query peut retourner des données projetées ou issues d'un index, mais la projection doit respecter les permissions et le contexte tenant du demandeur. Une donnée mise en cache ne doit jamais être servie à un sujet ou tenant non autorisé.

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

Les états de lifecycle sont des dimensions distinctes :

```text
installed
enabled
configured
ready
healthy
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

Une configuration, dépendance ou contrainte de compatibilité invalide doit empêcher l'activation ou le passage à `ready`. Une défaillance doit rester observable et ne doit pas supprimer implicitement les données.

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
scheduled_at éventuel
attempt_count
timeout éventuel
priority éventuelle
```

Ses états sont :

```text
PENDING
SCHEDULED
RUNNING
SUCCEEDED
RETRYING
FAILED
CANCELLED
DEAD_LETTER
```

Un Job n'est pas une autorité métier. Toute mutation déclenchée par un Job passe par une Command, avec validation, autorisation et transaction Django. Les handlers doivent être idempotents ou déclarer explicitement leurs limites. Les Jobs périodiques doivent être déclarés et versionnés.

Les données nécessaires à la reprise — état, tentatives, échéances, résultats et erreurs diagnostiquables — doivent être persistantes et compatibles avec la garantie `at-least-once`.

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

Les Commands sont exposées comme opérations de mutation et les Queries comme opérations de lecture. Chaque route doit déclarer son contrat, son schéma d'entrée, son schéma de sortie, ses erreurs, ses exigences d'authentification, son contexte tenant et ses permissions.

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

L'authentification HTTP standard est portée par l'en-tête `Authorization: Bearer`. Un provider peut valider un token OAuth2/OIDC JWT ou opaque et doit produire un contexte rattaché à une `DigitalIdentity`. Les API keys sont réservées aux mécanismes explicitement déclarés pour les comptes de service. Le mTLS peut être utilisé pour les identités `DEVICE` ou les comptes de service lorsque le provider le prend en charge.

L'autorisation ne doit être évaluée qu'après résolution de l'identité numérique, du contexte tenant et du contexte de requête. Un identifiant d'utilisateur présent dans le payload ou les paramètres ne modifie jamais le sujet authentifié. Une route sans authentification doit déclarer explicitement son caractère public dans son contrat API et appliquer malgré tout ses règles de validation et de limitation.

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

WebSocket et SSE sont des transports optionnels réservés aux capacités réactives. GraphQL et RPC peuvent être ajoutés comme adapters compatibles, mais ne sont pas requis par le Kernel ni par le contrat API principal.

Une API ne doit jamais exposer directement les modèles privés, repositories ou détails de persistance d'un module. Elle utilise les interfaces publiques, Commands, Queries, services et schémas déclarés.

## 26. Extension frontend

Le frontend de référence utilise TanStack, mais les frontières d'extension sont définies par des contrats frontend publics et versionnés plutôt que par les imports ou l'arborescence interne du shell.

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

Le shell conserve la responsabilité du lifecycle d'interface, du routage global, de l'authentification, du contexte tenant, de la gestion des erreurs, du chargement, du Design System et des garde-fous de sécurité. Une extension peut demander une donnée ou une action au travers des APIs, Commands, Queries et contrats UI publics ; elle ne peut pas modifier directement l'état métier, les ACL ou les modèles backend.

La résolution des contributions doit être déterministe, indépendante de l'ordre des imports et reproductible entre développement, build et runtime. Le lazy loading est une optimisation déclarée par la contribution et ne doit pas modifier les règles d'autorisation. Un adapter TanStack traduit les contrats frontend génériques en routes, composants et mécanismes de chargement propres à TanStack.

La distribution de référence est une composition au build. Le composant frontend d'un module est livré avec ses sources ou artefacts, son manifest et ses contraintes de compatibilité avec le shell. Le build résout les contributions et génère les bundles ou chunks nécessaires dans l'artefact Pixs. Le runtime ne doit pas exécuter de téléchargement, d'installation de dépendance ou d'évaluation de code distant pour activer une extension. Le lazy loading ne fait que différer le chargement d'un chunk déjà livré. Un adapter de module distant pourra définir une autre stratégie, mais devra conserver les contrats, signatures, versions, permissions et garanties de sécurité du registre frontend.

Les extensions frontend consomment uniquement les API publiques versionnées. Le shell expose deux abstractions distinctes :

```text
QueryClient    lecture via Query et API publiques
CommandClient  mutation via Command et API publiques
```

Un adapter peut générer les clients typés à partir d'OpenAPI. TanStack Query peut implémenter la gestion de l'état serveur, du cache, de l'invalidation et des retries, mais ne devient pas la source de vérité métier. Une clé de cache doit être déterminée par la version d'API, le tenant, l'identité lorsque pertinente, la ressource, les filtres, le tri et les autres paramètres validés. Une réponse ou projection Electric ne peut être utilisée que si la capacité déclare la réactivité et ne peut jamais remplacer la vérification d'autorisation backend. Les mutations optimistes représentent un état d'interface provisoire et doivent être réconciliées avec le résultat de la Command.

Le shell expose un contexte de session en lecture seule aux extensions :

```text
DigitalIdentity   identité authentifiée ou absence d'identité
User              utilisateur associé éventuellement
Tenant            tenant courant ou contexte plateforme
UIPermissions     permissions utiles à l'affichage
SessionState      initialisation, active, expirée, révoquée, erreur
```

Une extension ne doit pas accéder aux tokens bruts, les décoder ou les persister. Le token d'accès peut rester en mémoire pendant la session ; le renouvellement navigateur utilise, lorsque nécessaire, une session de renouvellement portée par un cookie `HttpOnly`, `Secure` et `SameSite` compatible avec la politique CSRF. `localStorage` et `sessionStorage` ne doivent pas contenir de token d'accès ou de renouvellement. Les guards de route et permissions UI sont des optimisations d'expérience, jamais des décisions d'autorisation. Lorsqu'un tenant courant change, le shell doit annuler ou invalider les requêtes, caches, projections et états locaux liés à l'ancien contexte avant d'exposer le nouveau.

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

## 35. Conformité des providers et capacités du point 12

Les contrats `ObjectStorageProvider`, `DocumentRepositoryProvider`, `SearchProvider` et `SynchronizationProvider` doivent disposer d'une suite de conformité versionnée. Cette suite vérifie les garanties du contrat, indépendamment de la technologie du provider. Le runtime ne doit pas déclarer compatible un provider dont la conformité obligatoire est absente, expirée ou échouée.

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

Une release Pixs est définie par sa version fonctionnelle, sa source, sa composition de composants, ses manifests, ses contrats et ses dépendances. Le paquet Debian et l'image OCI/Docker d'une même release doivent être corrélables et conserver les mêmes garanties fonctionnelles. Les artefacts publiés sont immuables ; une correction produit une nouvelle version ou un nouvel artefact explicitement corrélé.

La configuration, les références de secrets, PostgreSQL, les volumes persistants, les fichiers utilisateur et les stockages externes ne doivent pas être confondus avec l'artefact applicatif. Le runtime reçoit une configuration validée et ne doit pas déduire un provider, un tenant ou une identité de l'état accidentel du paquet, de l'image ou du filesystem éphémère.

Une mise à niveau est une opération orchestrée par Pixs et l'adapter d'exploitation :

```text
prévalidation de l'artefact et de la composition
    ↓
validation des contrats, dépendances et compatibilités
    ↓
validation du plan de migration
    ↓
exécution des migrations autorisées
    ↓
démarrage et validation startup
    ↓
readiness / health
    ↓
activation du trafic
```

Les migrations de données sont versionnées, possédées par les modules et orchestrées globalement. Une migration n'est pas annulée automatiquement pour simuler un rollback applicatif. Un downgrade est bloqué lorsqu'il n'existe pas de garantie explicite de compatibilité du code avec le schéma et les données actuels. Un rollback applicatif peut être proposé uniquement lorsque la matrice de compatibilité l'autorise ; sinon, la procédure de restauration doit être explicite, vérifiée et auditée.

Systemd, un runtime de conteneurs et un orchestrateur externe peuvent fournir des adapters d'exploitation différents, mais ils doivent alimenter le même lifecycle Pixs, les mêmes health checks, la même configuration validée, les mêmes signaux d'arrêt et les mêmes diagnostics. Aucun orchestrateur externe ne doit devenir une autorité métier ou une dépendance du Kernel.

Le runtime applicatif est stateless par défaut. Les processus web, workers et schedulers ne doivent pas conserver dans leur mémoire ou leur filesystem local un état nécessaire à l'autorité métier, à l'idempotence, à la reprise d'un Job, à une session durable ou à la synchronisation d'un tenant. PostgreSQL, l'outbox, les Jobs, les sessions et les stockages externes fournissent les mécanismes persistants nécessaires.

Une seule instance doit pouvoir fonctionner avec la même composition qu'un déploiement multi-instance. Les verrous, leases, déduplications, files et checkpoints doivent être coordonnés par une source persistante ; un verrou mémoire ou un fichier local ne peut être utilisé que comme optimisation sans garantie d'autorité. La montée en charge horizontale des rôles web, worker et scheduler ne doit pas modifier les contrats métier ni provoquer de double traitement non maîtrisé.

Les rôles d'exécution sont des profils du même artefact :

```text
web       API, sessions et trafic utilisateur
worker    Jobs, événements, notifications et synchronisations
scheduler planification périodique et déclenchement des Jobs
```

Le mode de développement peut regrouper plusieurs profils, mais un déploiement de production doit rendre leur activation, leurs capacités et leurs limites inspectables. Le scheduler acquiert un lease persistant avec durée, renouvellement et expiration contrôlés ; la perte du lease arrête ou suspend le déclenchement. Les workers consomment des Jobs persistants et s'appuient sur l'idempotence, la déduplication et les limites de concurrence pour supporter la réplication.

## 37. Sauvegarde et reprise après sinistre

Pixs ne prescrit pas un outil de sauvegarde, mais expose les éléments nécessaires à une stratégie de récupération déclarée par déploiement. Le déploiement doit définir ses objectifs `RPO` et `RTO`, son périmètre, ses durées de conservation, ses contrôles d'accès, ses procédures de restauration et la preuve attendue après restauration.

La stratégie doit couvrir séparément :

```text
PostgreSQL
    modèles, migrations appliquées, outbox, Jobs, idempotence,
    workflows, mappings, audit et configuration persistée

stockages objet et fichiers
    contenu, versions, rétention, legal holds et checksums

configuration et secrets
    références, versions, accès et mécanismes de rotation
```

Une sauvegarde ne devient pas une nouvelle source d'autorité. Une restauration doit vérifier la cohérence entre les métadonnées PostgreSQL, les objets binaires, les événements non publiés, les Jobs, les checkpoints, les mappings externes et les versions de composants. Les identités, tenants, ACL, secrets, fichiers et données métier ne doivent pas être réinitialisés ou supprimés implicitement pour rendre la restauration possible.

Les restaurations doivent être exécutables dans un environnement isolé et testées régulièrement. Après restauration, Pixs doit pouvoir démarrer en état contrôlé, détecter les écarts de composition ou de version, reprendre les traitements idempotents et maintenir les événements ou synchronisations non confirmés dans un état diagnostiquable. Une restauration destructive ou un retour à un point antérieur nécessite une opération explicitement autorisée et auditée.

Le lifecycle de déploiement doit supporter une mise à niveau avec interruption courte. Les modes rolling, blue/green et canary sont des stratégies d'adapter et ne constituent pas une garantie du Kernel. Un mode progressif exige une compatibilité transitoire entre les versions `N` et `N+1` pour les API, événements, schémas et données partagés ; les migrations suivent lorsque nécessaire une séquence d'expansion, de double compatibilité, puis de contraction. Une suppression de colonne, d'index, de contrat ou de champ consommé par `N` est différée jusqu'à la fin de la fenêtre de compatibilité.

Le contrôleur d'exploitation doit pouvoir distinguer préparation, exposition, activation, retrait et rollback. Une instance qui échoue ses probes ou ses contrôles de compatibilité ne reçoit pas de trafic et ne doit pas être considérée comme une cible valide de rollback sans vérification du schéma et des données.

Une mise à jour applicative est une opération explicitement demandée par un opérateur ou un système d'exploitation autorisé. Le runtime ne doit pas télécharger, installer ou activer silencieusement une nouvelle composition. Avant l'exécution, le plan doit indiquer la release cible, la provenance, les migrations, les contrats affectés, les préconditions, la stratégie de déploiement et les possibilités de reprise. Après l'exécution, il doit conserver le résultat, les diagnostics, les versions actives et les décisions de rollback.

Un mécanisme de mise à jour de sécurité fourni par Debian, le runtime de conteneurs ou un orchestrateur peut automatiser le déclenchement, mais ne supprime pas la validation de signature, provenance, compatibilité, configuration, migrations, health checks et état de récupération. Une mise à jour refusée ou interrompue doit laisser l'ancienne composition ou un état explicitement sûr, sans purge ni activation partielle non diagnostiquée.

Chaque release doit déclarer ses origines compatibles, ses migrations requises, les versions intermédiaires éventuelles et les conditions de sortie de support. La chaîne de migration est ordonnée et vérifiable ; un saut de version n'est permis que si toutes les migrations et garanties intermédiaires sont compatibles ou regroupées explicitement dans le plan. Une version hors fenêtre de support ou sans chemin de migration vérifiable doit être refusée avant modification des données.

Les canaux de publication sont des contextes de confiance distincts :

```text
stable
    releases fonctionnelles validées et supportées

security
    corrections de sécurité compatibles avec une release supportée

experimental
    essais explicitement sélectionnés, sans garantie de compatibilité stable
```

Le canal, la version, la source, la composition et le digest éventuel doivent être vérifiables avant installation. Le runtime ne doit pas considérer un tag mutable ou le canal expérimental comme équivalent à une release stable. Un artefact d'un canal non autorisé doit être refusé avant activation.

La signature, la provenance et le SBOM d'un artefact font partie de son identité de distribution. Le trust store, les clés autorisées, leur rotation et leur révocation sont gérés par une capacité de sécurité ou l'adapter d'exploitation, jamais par une valeur secrète intégrée à l'image ou au paquet. La vérification doit être exécutée avant installation, démarrage et mise à niveau ; une signature invalide, absente, expirée ou révoquée bloque l'opération et produit un diagnostic sans exposer de secret.

L'autorité de signature des canaux `stable` et `security` doit être distincte de celle des artefacts `experimental`, sauf décision de confiance explicitement documentée. Le trust store peut être distribué avec l'environnement d'exploitation ou fourni par une capacité de sécurité, mais sa modification est versionnée, autorisée et auditée. Une rotation doit permettre une période de chevauchement contrôlée ; une révocation doit rester vérifiable même lorsqu'un dépôt ou un service de publication est indisponible. Les clés privées ne doivent être accessibles qu'au processus de signature autorisé et ne doivent apparaître dans aucun artefact, log, manifest ou fixture.

## 38. Interface d'exploitation

L'exploitation repose sur une interface de management distincte de l'API métier. Elle peut être consommée par une CLI officielle, une interface HTTP d'administration ou un adapter d'orchestrateur, mais ces façades utilisent les mêmes contrats et la même autorité.

Les opérations doivent pouvoir couvrir :

```text
inspect
validate
plan
migrate
upgrade
rollback autorisé
restart contrôlé
health
diagnostic
```

Une opération d'exploitation porte son identifiant, sa version, son acteur, son contexte plateforme ou tenant, son périmètre, sa clé d'idempotence, son plan, son état et son résultat. Les mutations sensibles exigent une confirmation ou une étape d'application distincte de la génération du plan. Les opérations longues retournent un suivi persistant et utilisent les Jobs lorsque nécessaire.

La CLI et l'API d'exploitation ne doivent pas exposer de secret, token, clé privée, valeur de configuration secrète ou payload sensible dans leur sortie standard, leurs réponses, leurs logs ou leurs diagnostics. Les commandes non interactives doivent produire des codes de sortie et des erreurs stables afin d'être utilisées par un pipeline. Une opération non autorisée, ambiguë ou non idempotente doit échouer explicitement plutôt que simuler un succès.

`MAINTENANCE` est un état d'exploitation distinct des états métier et du lifecycle d'un composant. Il doit pouvoir porter une cause, un acteur, un périmètre, une durée ou condition de sortie et une corrélation. En maintenance :

```text
mutations métier              bloquées ou limitées explicitement
lectures                      autorisées selon la politique déclarée
Jobs                          drainés, suspendus ou repris selon leur contrat
synchronisations              suspendues ou placées en état contrôlé
health                        expose l'état et la capacité à reprendre
management                    accessible aux opérateurs autorisés
```

La mise en maintenance doit pouvoir drainer les traitements en cours avant de bloquer les nouvelles mutations, avec un délai borné et un résultat diagnostiquable. Une requête métier reçue pendant cette phase répond par un état contractuel stable ; elle ne doit pas être exécutée partiellement. La sortie de maintenance réévalue la configuration, la composition, les migrations, les dépendances et les permissions avant de réactiver le trafic.

Par défaut, `MAINTENANCE` autorise uniquement les Queries explicitement compatibles avec la lecture seule. Les Commands métier, les Commands asynchrones, les Jobs et les synchronisations sont refusés ou suspendus selon leur contrat. La frontière API doit produire une représentation stable de l'état de maintenance, sans exposer de détail sensible, et le client ne doit pas interpréter un refus de maintenance comme un échec métier définitif. Une capacité peut déclarer une opération d'administration ou de sécurité autorisée pendant la maintenance ; cette exception est indépendante des mutations métier ordinaires et reste auditée.
## 39. Providers concrets et modules métier

Les providers et modules métier sont des `Component` versionnés. Leur manifest doit déclarer leurs capacités fournies et requises, contrats implémentés, dépendances, configuration, compatibilité, lifecycle, niveau de confiance et tests de conformité applicables.

Les niveaux de confiance conceptuels sont :

```text
CORE       mécanisme intégré au Kernel ou à pixs.core
OFFICIAL   provider ou module maintenu et distribué officiellement par Pixs
EXTERNAL   composant tiers installé depuis une source déclarée
PRIVATE    composant propre à une installation ou organisation
```

`CORE` ne doit pas être utilisé pour masquer une implémentation métier ou un provider concret. Un composant `OFFICIAL` peut être livré dans un artefact Pixs, mais reste soumis à son propre versionnement, lifecycle, configuration, signature et sélection. Les composants `EXTERNAL` et `PRIVATE` doivent fournir les mêmes contrats publics et garanties de sécurité que les composants officiels lorsqu'ils prétendent être compatibles.

Le resolver ne doit jamais activer automatiquement un provider parce qu'il est présent sur le filesystem, importable ou livré dans l'image. La résolution suit la configuration explicite, puis un candidat compatible unique ; plusieurs candidats ou l'absence d'un provider requis produisent une composition invalide. Un fallback concret doit être déclaré comme une composition ou une politique de capacité et ne peut pas être déduit silencieusement.

`pixs.core` fournit les primitives transverses — identité, tenant, autorisation, configuration, lifecycle, contrats et persistance commune — sans porter les invariants d'un domaine métier particulier. Un module métier possède ses modèles, migrations, permissions, Commands, Queries, Events et invariants. Un autre module ne peut pas écrire directement ses tables ou importer son implémentation privée ; il utilise ses interfaces publiques.

Un module métier peut requérir un provider ou une capacité concrète, mais cette dépendance doit être déclarée, versionnée et justifiée. Les providers d'intégration externe restent des adapters : ils traduisent un protocole ou un service sans déplacer automatiquement la source de vérité métier hors de Pixs.
