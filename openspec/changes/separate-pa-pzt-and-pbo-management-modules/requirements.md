# Références normatives — separate-pa-pzt-and-pbo-management-modules

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Références courantes du périmètre validé

Les copies plus anciennes conservées dans ce fichier sont historiques. Seuls les blocs ci-dessous correspondent au référentiel de la cible consolidée. Ils ne sont pas des deltas à synchroniser et ne prouvent aucune implémentation.

| Capacité | Exigence | Scénarios | Référence |
|---|---|---:|---|
| pixs-agent | Supervision PBO et collecte PA | 2 | pixs-agent-33fea834fa00 |
| pixs-agent | Contrats publics de pixs.agent et propriété des opérations | 1 | pixs-agent-9e3626c5a78b |
| pixs-agent | Interfaces de gestion PA au-dessus du socle | 1 | pixs-agent-8d8641f2c69b |
| pixs-agent | Liaison serveur persistante du contexte Agent et PA | 1 | pixs-agent-6e0e97f88daf |
| pixs-agent | Contexte initial PA distinct de la gestion ordinaire Agent | 1 | pixs-agent-42a32e0a6e53 |
| pixs-agent | Phases PA et issues Agent séparées avec projection conditionnelle | 4 | pixs-agent-b21bbc0cc084 |
| pixs-agent | Fournisseurs PA PZT retenus et disponibilité démontrée | 3 | pixs-agent-b8800e3e3ca6 |
| pzt | Module essentiel pixs.pzt et exécutable PZT indépendant | 1 | pzt-1063497b290f |
| pzt | Passage obligatoire PBO–PA par PZT | 1 | pzt-d043fc6da2c1 |
| pzt | Contrôle de PZT et séparation de pixs.agent | 1 | pzt-697493dc12e0 |
| pzt | Frontières et identités PA PZT explicites | 1 | pzt-0f4a5ba6eba9 |
| scope-context | Périmètre explicite du Super Admin | 1 | scope-context-20a18bf192a8 |
| scope-context | Tenant racine et parenté unique | 1 | scope-context-49cd4f07132a |
| scope-context | Propriété canonique unique | 1 | scope-context-3a23c52bedfb |
| scope-context | Contexte immuable propagé avant autorisation | 3 | scope-context-a568773185f8 |
| scope-context | Propagation et frontière d'autorisation du ScopeContext | 3 | scope-context-24734273be96 |
| managed-device-policies | Cibles V1 et exécutants locaux | 1 | managed-device-policies-8a43d725b9c8 |
| managed-device-policies | Gestion ZT et jonction d’authentification distinctes | 1 | managed-device-policies-f3d868c20f8b |
| managed-device-policies | Politiques communes et spécifiques | 1 | managed-device-policies-0fc04bee903f |
| managed-device-policies | Priorités et contradictions | 1 | managed-device-policies-a7f801c0bbd9 |
| managed-device-policies | Application par PA et état vérifié | 1 | managed-device-policies-fc87e0db8071 |
| managed-device-policies | Session hors ligne bornée | 1 | managed-device-policies-53ac3cf3063d |
| managed-device-policies | Rotation des secrets machine et services | 1 | managed-device-policies-0e3d3ee17150 |
| managed-device-policies | Redémarrage par profil et conclusion après reprise | 1 | managed-device-policies-0a228d3c9bf5 |

### Référence courante pixs-agent-33fea834fa00

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 229. SHA-256 : `33fea834fa000e71689e0fc02880468b368455df3d56c7edd066643d87e6a676`.

Scénarios : Collecte PA interrompue; Gestion PZT exclue de pixs.agent.

~~~~text
### Requirement: Supervision PBO et collecte PA

Le module PBO pixs.agent MUST configurer, administrer et superviser toutes les
fonctions PA hors PZT. PA MUST rapporter ses mesures, versions et états réels
via PZT ; pixs.agent MUST distinguer état souhaité, appliqué, dernier état connu
et résultat confirmé. La gestion réseau MUST rester dans pixs.pzt. Une mesure
ancienne MUST être datée et MUST NOT devenir un état courant sans preuve.

#### Scenario: Collecte PA interrompue

- **WHEN** la collecte PA est interrompue alors que le dernier état était sain
- **THEN** pixs.agent signale les mesures périmées sans déduire une disponibilité actuelle

#### Scenario: Gestion PZT exclue de pixs.agent

- **WHEN** une configuration du composant réseau PZT est demandée
- **THEN** la gestion relève de pixs.pzt et aucune mutation PZT n’est attribuée à pixs.agent
~~~~

### Référence courante pixs-agent-9e3626c5a78b

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 397. SHA-256 : `9e3626c5a78b292c9bfa54b50fe1186795b67dec326726372ee6cb4a7fc8f30f`.

Scénarios : Module sollicitant une opération PA.

~~~~text
### Requirement: Contrats publics de pixs.agent et propriété des opérations

Les modules fonctionnels MUST solliciter PA via les contrats publics versionnés
de pixs.agent et MUST conserver la propriété de leurs opérations et règles métier.
pixs.agent MUST exposer les fonctions de gestion PA hors PZT et le suivi des
instructions, états et résultats. Il MUST NOT absorber les opérations métier,
le transport PZT ou les données privées d'un autre module.

#### Scenario: Module sollicitant une opération PA

- **WHEN** un module fonctionnel demande une opération système autorisée
- **THEN** il utilise le contrat pixs.agent, garde ses règles métier et suit un résultat PA distinct de l'accusé de réception
~~~~

### Référence courante pixs-agent-8d8641f2c69b

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 410. SHA-256 : `8d8641f2c69bbde3c139b28dc2627bb3ba71508c8f05fa4abd771d2d1ff550d1`.

Scénarios : Sollicitation locale via pixs.agent.

~~~~text
### Requirement: Interfaces de gestion PA au-dessus du socle

pixs.agent MUST utiliser les mécanismes communs de composition et les contrats
pixs.core d'identité et de permissions. Ses données de gestion, contrats,
permissions, contributions frontend et lifecycle MUST être déclarés. Le Kernel et pixs.core MUST NOT porter une logique de gestion ou de transport
spécifique à PA. Tous les échanges PBO–PA MUST passer par PZT, même localement.

#### Scenario: Sollicitation locale via pixs.agent

- **WHEN** le PBO et le PA partagent un environnement d'exécution
- **THEN** pixs.agent utilise PZT et aucun canal local de substitution n'est ouvert
~~~~

### Référence courante pixs-agent-6e0e97f88daf

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 521. SHA-256 : `6e0e97f88daf6093b9b5634f5fbefdecee2482ca0eb9657f9ecdaebff86cf690`.

Scénarios : Liaison absente ou divergente.

~~~~text
### Requirement: Liaison serveur persistante du contexte Agent et PA

En gestion ordinaire, pixs.agent MUST posséder une liaison persistante côté serveur entre opération, cible, scope, génération Agent et références techniques PA/C08, sous contrôle des propriétaires. Une liaison absente, périmée ou divergente MUST être refusée. Une donnée client MUST NOT suffire à établir cette liaison ; les compteurs natifs PA MUST rester distincts de la génération Agent.

#### Scenario: Liaison absente ou divergente

- **WHEN** un résultat technique est présenté sans liaison serveur courante correspondant à son opération, sa cible, son scope et sa génération Agent
- **THEN** son rapprochement avec l'état Agent est refusé sans déduire une génération depuis un compteur natif ou une déclaration cliente
~~~~

### Référence courante pixs-agent-42a32e0a6e53

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 530. SHA-256 : `42a32e0a6e532a6ecd6416c34692c772f80f3e1756477b371d0dd3cc49338f84`.

Scénarios : Amorçage avant disponibilité du contexte Agent.

~~~~text
### Requirement: Contexte initial PA distinct de la gestion ordinaire Agent

L'amorçage avant PostgreSQL MUST conserver son contexte initial C08/PA. Il MUST NOT créer une génération Agent fictive pour satisfaire la liaison de gestion ordinaire. La décision de liaison serveur MUST NOT ajouter implicitement de champs aux messages PA existants ; sa structure et ses règles de mise à jour MUST être spécifiées conjointement par PA01/C08/PA10 avant réalisation dépendante.

#### Scenario: Amorçage avant disponibilité du contexte Agent

- **WHEN** C08 et PA exécutent le parcours initial avant PostgreSQL et les autorités Agent requises
- **THEN** ils conservent le contexte initial propriétaire sans fabriquer de génération ou d'autorité Agent
~~~~

### Référence courante pixs-agent-b21bbc0cc084

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 539. SHA-256 : `b21bbc0cc0846c7c03bd621239aebb5ede22bdfdfedec7c6fa3b87655e810804`.

Scénarios : Réception ou progression sans fait appliqué; Succès technique sans confirmation automatique; Échec connu et issue incertaine distincts; Précondition refusée sans échec d'exécution fabriqué.

~~~~text
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
~~~~

### Référence courante pixs-agent-b8800e3e3ca6

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 1278. SHA-256 : `b8800e3e3ca616cda506afe36218fdc6cf7d071e8b60f5aab99fea59d2098eb1`.

Scénarios : Interface présente et fournisseur requis absent; Résultat natif sans postcondition vérifiée; Producteur temporel manquant dans un processus.

~~~~text
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
~~~~

### Référence courante pzt-1063497b290f

Source : [pzt](../../specs/pzt/spec.md), ligne 77. SHA-256 : `1063497b290fd7bb8e8abad2dad81ac19bb67f139b4c911c98be000279df7b7c`.

Scénarios : Réseau désactivé et gestion conservée.

~~~~text
### Requirement: Module essentiel pixs.pzt et exécutable PZT indépendant

Toute composition cible PBO MUST inclure le module officiel essentiel pixs.pzt,
au-dessus du Kernel et de pixs.core, par les mécanismes génériques. pixs.pzt
MUST configurer, administrer, visualiser, superviser et monitorer PZT. Le réseau
activé/configuré MUST être exécuté par le binaire indépendant PZT, compilé avec
Cython. Désactiver le réseau MUST NOT retirer pixs.pzt de PBO.

#### Scenario: Réseau désactivé et gestion conservée

- **WHEN** PZT est désactivé dans un PBO
- **THEN** le binaire réseau se ferme mais pixs.pzt demeure composé avec ses fonctions de gestion
~~~~

### Référence courante pzt-d043fc6da2c1

Source : [pzt](../../specs/pzt/spec.md), ligne 90. SHA-256 : `d043fc6da2c1af6b20ea6e3d132cef7ef964e1df6b38e09fba4b82a2d52b1955`.

Scénarios : Passage obligatoire PBO–PA par PZT.

~~~~text
### Requirement: Passage obligatoire PBO–PA par PZT

Tous les échanges PBO–PA, instructions, configuration, administration, états, diagnostics, événements et résultats MUST passer par PZT dans les deux sens, même sur le même hôte ou conteneur. Le transport local mTLS MUST conserver identification, autorisation, chiffrement, validité, anti-rejeu et traçabilité ; WireGuard local n'est pas obligatoire. Un profil local indisponible MUST NOT déclencher un canal Unix, loopback ou fichier de substitution hors PZT.

#### Scenario: Passage obligatoire PBO–PA par PZT

- **WHEN** le transport local PZT n'est pas vérifiable
- **THEN** le contrôle PBO–PA concerné est bloqué sans repli de proximité
~~~~

### Référence courante pzt-697493dc12e0

Source : [pzt](../../specs/pzt/spec.md), ligne 257. SHA-256 : `697493dc12e0eeeb23f25f8e87a71007080c4521c1d42e0bdaa3e30c2a1a5202`.

Scénarios : Administration du réseau depuis PBO.

~~~~text
### Requirement: Contrôle de PZT et séparation de pixs.agent

Les échanges de configuration, administration, supervision et monitoring du
binaire PZT MUST relever des contrats publics sécurisés de pixs.pzt. pixs.agent
MUST gérer PA hors PZT et consommer le transport PZT sans l'administrer. Un
contrat de gestion MUST conserver cible, droits, validité et résultat observé ;
il MUST NOT ouvrir de canal PBO–PZT ou PBO–PA hors des contrôles PZT.

#### Scenario: Administration du réseau depuis PBO

- **WHEN** un opérateur demande une modification PZT autorisée
- **THEN** pixs.pzt porte la gestion et PZT exécute puis rapporte l'état réellement appliqué
~~~~

### Référence courante pzt-0f4a5ba6eba9

Source : [pzt](../../specs/pzt/spec.md), ligne 270. SHA-256 : `0f4a5ba6eba942fd067ab81877191eb5886e0811f8f2bf48fbd6a02aaa59d610`.

Scénarios : Colivraison sans admission du composant réseau.

~~~~text
### Requirement: Frontières et identités PA PZT explicites

Les profils MUST déclarer les interfaces PA–PZT, appelants, cibles, droits,
isolation et liaisons d'identités et de preuves requises. PA et PZT MUST garder
leurs identités, clés et états distincts. Une colivraison ou une attestation PA
MUST NOT admettre automatiquement PZT, transférer un secret, un privilège ou
supprimer une preuve d'identité, d'hôte ou d'intégrité exigée.

#### Scenario: Colivraison sans admission du composant réseau

- **WHEN** PA et PZT sont installés ensemble mais une preuve requise pour PZT n'est pas vérifiable
- **THEN** le périmètre dépendant est bloqué sans identité partagée ni transfert implicite de droit
~~~~

### Référence courante scope-context-20a18bf192a8

Source : [scope-context](../../specs/scope-context/spec.md), ligne 8. SHA-256 : `20a18bf192a8b52d7e7a3ae6628f6b82dea2833869a146235d4f667c9725c213`.

Scénarios : Accord tenant sans changement de propriété.

~~~~text
### Requirement: Périmètre explicite du Super Admin

L'exception Super Admin MUST suivre `authorization` sans modifier la structure du ScopeContext ni la propriété canonique des ressources. Le contrôle total tenant-scoped MUST exiger un accord explicite préalable pour le tenant concerné. Les exigences d'audit de périmètre MUST rester dérogeables pour ce seul compte selon `audit`.

#### Scenario: Accord tenant sans changement de propriété

- **WHEN** le Super Admin reçoit un accès explicite au tenant A puis agit malgré une ACL de A
- **THEN** le ScopeContext reste TENANT avec le tenant A et la ressource conserve sa propriété canonique
- **AND** un tenant B non accordé reste hors de son périmètre
~~~~

### Référence courante scope-context-49cd4f07132a

Source : [scope-context](../../specs/scope-context/spec.md), ligne 18. SHA-256 : `49cd4f07132ad31022e1f642726b4a08752a7abd67a12d9933e2b3c0308d15c9`.

Scénarios : Cycle de scopes refusé.

~~~~text
### Requirement: Tenant racine et parenté unique

Chaque tenant MUST rester la racine de ses scopes enfants ; chaque scope enfant MUST avoir un parent unique dans ce tenant sans cycle. En mode Domaine, chaque tenant MUST appartenir à un seul Domaine selon pixs-domains. Les périmètres Instance et Domaine MUST rester distincts de la hiérarchie interne des scopes tenant.

#### Scenario: Cycle de scopes refusé

- **WHEN** une parenté crée un cycle ou rattache un scope à un autre tenant
- **THEN** la déclaration est refusée avant activation.
~~~~

### Référence courante scope-context-3a23c52bedfb

Source : [scope-context](../../specs/scope-context/spec.md), ligne 27. SHA-256 : `3a23c52bedfbfa5d0ae6a079534b9a15da12cd0b14ebc79d7a89147247978542`.

Scénarios : Scope sans tenant cohérent refusé.

~~~~text
### Requirement: Propriété canonique unique

Chaque ressource MUST avoir une propriété canonique unique : Instance, Domaine, Tenant ou scope enfant cohérent. En mode Domaine, un tenant propriétaire MUST référencer son Domaine. Partage, délégation et ACL MUST NOT changer cette propriété ou permettre un accès implicite. Les références historiques PLATFORM MUST être distinguées du nouveau contexte versionné.

#### Scenario: Scope sans tenant cohérent refusé

- **WHEN** un scope propriétaire ne correspond pas au tenant déclaré
- **THEN** la mutation est refusée sans accès à un autre périmètre.
~~~~

### Référence courante scope-context-a568773185f8

Source : [scope-context](../../specs/scope-context/spec.md), ligne 36. SHA-256 : `a568773185f8eea21b482e1bf41a3c33896e6fad732c43e8eb93d16f8763ed93`.

Scénarios : Contexte TENANT sans tenant refusé; Contexte PLATFORM avec identifiants refusé; Nouveau parcours Domaine sur contexte incomplet.

~~~~text
### Requirement: Contexte immuable propagé avant autorisation

Le contexte MUST être versionné et résolu avant autorisation, avec propriétaire Instance/Domaine/Tenant et scope cohérent lorsque requis. Les contrats v1 MUST conserver leur vocabulaire TENANT/PLATFORM et leurs validations ; les parcours Domaine MUST employer un contrat explicitement adapté/versionné et MUST NOT prétendre qu'un contexte v1 sans référence Domaine suffit à les qualifier. Pour v1 TENANT, tenant_id MUST être présent et scope_id cohérent ; pour v1 PLATFORM les deux MUST être absents.

#### Scenario: Contexte TENANT sans tenant refusé

- **WHEN** un contexte v1 TENANT omet tenant_id
- **THEN** sa structure est refusée.

#### Scenario: Contexte PLATFORM avec identifiants refusé

- **WHEN** un contexte v1 PLATFORM contient tenant_id ou scope_id
- **THEN** sa structure est refusée.

#### Scenario: Nouveau parcours Domaine sur contexte incomplet

- **WHEN** un parcours exige une référence Domaine non résolue par son contrat
- **THEN** l’accès est bloqué sans l’inférer d’un champ client ou d’une plateforme implicite.
~~~~

### Référence courante scope-context-24734273be96

Source : [scope-context](../../specs/scope-context/spec.md), ligne 55. SHA-256 : `24734273be961e63f77378a58b4027d3469843b00bada4ee705920c8aeb51557`.

Scénarios : Élargissement implicite refusé; Contexte PLATFORM sans identifiants accepté sans octroyer permission; Accès plateforme sans permission refusé et audité.

~~~~text
### Requirement: Propagation et frontière d'autorisation du ScopeContext

Le contexte structurellement valide MUST NOT valoir autorisation : tout accès plateforme exige permission, contexte et audit explicites. Le contexte est résolu avant l'autorisation, immuable pendant l'opération et propagé aux commandes, requêtes, événements, travaux, caches, fichiers, recherches et audits ; aucun élargissement implicite.

#### Scenario: Élargissement implicite refusé

- **WHEN** un en-tête ou un identifiant client prétend élargir le périmètre
- **THEN** le contexte canonique prévaut et tout accès hors périmètre est refusé et audité

#### Scenario: Contexte PLATFORM sans identifiants accepté sans octroyer permission

- **WHEN** un ScopeContext déclare PLATFORM sans tenant_id ni scope_id
- **THEN** sa structure est acceptée sans octroyer aucune permission implicite

#### Scenario: Accès plateforme sans permission refusé et audité

- **WHEN** un accès plateforme est demandé sans permission explicite
- **THEN** l'accès est refusé et audité
~~~~

### Référence courante managed-device-policies-8a43d725b9c8

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 11. SHA-256 : `8a43d725b9c8f9f725eb22c048e5e91d1ee208d3af98a44e61ea75cfae643633`.

Scénarios : Poste administré.

~~~~text
### Requirement: Cibles V1 et exécutants locaux

Les profils V1 MUST couvrir postes Linux/Windows et serveurs Linux membres, avec Debian stable et Windows 10/11 admissibles à qualifier. Les postes administrés et serveurs Linux soumis aux politiques MUST disposer de PA/PZT locaux. Les rôles serveur de domaine MUST NOT être imposés sur chaque poste.

#### Scenario: Poste administré

- **WHEN** un poste reçoit une politique Pixs
- **THEN** les exécutants locaux sont vérifiés sans le transformer en LZT ou KZT.
~~~~

### Référence courante managed-device-policies-f3d868c20f8b

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 20. SHA-256 : `f3d868c20f8b51c27e721a1df72180c8508e9cfdf1ff06948b8294b817119a29`.

Scénarios : Hôte tiers géré.

~~~~text
### Requirement: Gestion ZT et jonction d’authentification distinctes

Un hôte MAY être intégré à ZT et administré sans jonction de domaine pour l'authentification de ses utilisateurs. Cette jonction MUST rester facultative mais exiger l'intégration ZT préalable lorsqu'elle est demandée. Le passage du PA en mode Domaine MUST NOT joindre automatiquement l'hôte au domaine d'authentification.

#### Scenario: Hôte tiers géré

- **WHEN** un hôte rejoint ZT sans jonction d’authentification
- **THEN** PA peut gérer ses capacités autorisées tandis que les utilisateurs conservent l’authentification configurée sur l’hôte.
~~~~

### Référence courante managed-device-policies-0fc04bee903f

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 29. SHA-256 : `0fc04bee903fa7c526db55656c40db141fc78bd93e1a2f658507d54be92da507`.

Scénarios : Règle propre à Windows.

~~~~text
### Requirement: Politiques communes et spécifiques

Les politiques MUST permettre des intentions communes Windows/Linux et des règles propres aux plateformes, avec politiques de poste et d'utilisateur et ciblage explicite. Les capacités non qualifiées MUST être déclarées non applicables ou indisponibles, sans simulation de succès.

#### Scenario: Règle propre à Windows

- **WHEN** une politique commune comporte une règle GPO Windows
- **THEN** l’application Linux ne prétend pas avoir appliqué cette règle native.
~~~~

### Référence courante managed-device-policies-a7f801c0bbd9

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 38. SHA-256 : `a7f801c0bbd9d9343d1e85e137ebc5eb30e56d499daabeba1006d7fe6d26ebbe`.

Scénarios : Deux valeurs au même niveau.

~~~~text
### Requirement: Priorités et contradictions

Les politiques de configuration MUST avoir des priorités explicites ; les contradictions à priorité égale MUST être signalées sans règle implicite du dernier reçu. La résolution MUST respecter les contrats de propriété et autorisations de chaque périmètre.

#### Scenario: Deux valeurs au même niveau

- **WHEN** deux politiques de même priorité imposent des valeurs incompatibles
- **THEN** l’écart est signalé et aucune valeur n’est choisie par ordre d’arrivée.
~~~~

### Référence courante managed-device-policies-fc87e0db8071

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 47. SHA-256 : `fc87e0db80717cda5b2c979b05d5045ee0bf334a5dd2cf6559bb9d13857e9c0e`.

Scénarios : Configuration reçue sans effet.

~~~~text
### Requirement: Application par PA et état vérifié

PA MUST appliquer les opérations livrées et autorisées dans le contexte système ou utilisateur approprié via pixs.agent. Réception, application, dérive et résultat confirmé MUST rester distincts. Les corrections automatiques MUST posséder leur propre politique et mandat.

#### Scenario: Configuration reçue sans effet

- **WHEN** PA reçoit une politique mais échoue à la mettre en place
- **THEN** PBO affiche l’échec sans état appliqué fictif.
~~~~

### Référence courante managed-device-policies-53ac3cf3063d

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 56. SHA-256 : `53ac3cf3063d580b57f56441ca276f52645441d643d76c41f8e4077b7e5882e7`.

Scénarios : Pas de profil hors ligne.

~~~~text
### Requirement: Session hors ligne bornée

L'ouverture de session hors ligne MAY être permise par profil explicite et borné. Elle MUST conserver les exigences de validité, protection locale et retraits connus ; une panne MUST NOT activer ce profil ni repousser ses échéances.

#### Scenario: Pas de profil hors ligne

- **WHEN** le contrôleur est indisponible sans profil hors ligne autorisé
- **THEN** aucune nouvelle permission de connexion locale n’est déduite de la panne.
~~~~

### Référence courante managed-device-policies-0e3d3ee17150

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 65. SHA-256 : `0e3d3ee171504e6660c5650982a199dc41378de37affda7cbe83cb40f3506336`.

Scénarios : Rotation native autorisée.

~~~~text
### Requirement: Rotation des secrets machine et services

La rotation des secrets machine MUST être sélectionnable par profil entre pilotage Pixs/PBO/PA et rotation native qualifiée. Les services techniques MUST pouvoir utiliser un moyen propre ou une représentation habilitée selon profil. Ces secrets MUST rester distincts du mot de passe des individus changé depuis PBO.

#### Scenario: Rotation native autorisée

- **WHEN** un poste utilise la rotation machine native qualifiée
- **THEN** elle suit son profil et sa cohérence contrôleurs sans autoriser un changement natif du mot de passe individuel.
~~~~

### Référence courante managed-device-policies-0a228d3c9bf5

Source : [managed-device-policies](../../specs/managed-device-policies/spec.md), ligne 74. SHA-256 : `0a228d3c9bf5969235d9a1b17bf8161742513eb0cd8bfd88e93f3901641b2177`.

Scénarios : Jonction exigeant redémarrage.

~~~~text
### Requirement: Redémarrage par profil et conclusion après reprise

Le profil MUST choisir redémarrage manuel ou automatique sous fenêtre autorisée, avec manuel par défaut. PBO MUST distinguer redémarrage requis et opération terminée ; les vérifications après redémarrage MUST précéder la conclusion de jonction ou de politique.

#### Scenario: Jonction exigeant redémarrage

- **WHEN** la configuration est appliquée mais le poste n’a pas redémarré
- **THEN** l’opération reste à terminer jusqu’aux contrôles après reprise.
~~~~
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

## Statut des deltas antérieurs après contrôle E3

Les anciens fichiers sous specs/ ont été déplacés, avec empreintes conservées, vers [l’historique interne](historique-deltas-avant-e3/README.md). Le [contrôle de couverture](COUVERTURE_DELTAS_E3.md) relie chaque ancienne exigence au contrat courant et aux tâches ouvertes. Le dossier reste actif ; skip_specs évite seulement la réapplication des anciennes prescriptions. Il ne termine ni la réalisation, ni les tests, ni les 49 tâches encore ouvertes dans les sept dossiers concernés.
