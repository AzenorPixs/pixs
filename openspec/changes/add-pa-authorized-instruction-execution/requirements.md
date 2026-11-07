# Références normatives — PA04

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Références courantes du périmètre validé

Les copies plus anciennes conservées dans ce fichier sont historiques. Seuls les blocs ci-dessous correspondent au référentiel de la cible consolidée. Ils ne sont pas des deltas à synchroniser et ne prouvent aucune implémentation.

| Capacité | Exigence | Scénarios | Référence |
|---|---|---:|---|
| pixs-agent | Unicité des opérations PA multiprocessus | 1 | pixs-agent-b22610f19af3 |
| pixs-agent | Composition au build et catalogue fermé | 1 | pixs-agent-0ed896227fd4 |
| pixs-agent | Contrat public des instructions et revalidation | 1 | pixs-agent-1760abaea35a |
| pixs-agent | Exécution locale et états indéterminés | 1 | pixs-agent-ff6703508e08 |
| pixs-agent | Plans sensibles et compensation préautorisée | 1 | pixs-agent-4ad8f35c03d3 |
| pixs-agent | Audit, confidentialité et exception Super Admin | 1 | pixs-agent-314ad93363d9 |
| pixs-agent | Liaison serveur persistante du contexte Agent et PA | 1 | pixs-agent-6e0e97f88daf |
| pixs-agent | Phases PA et issues Agent séparées avec projection conditionnelle | 4 | pixs-agent-b21bbc0cc084 |
| pzt | Passage obligatoire PBO–PA par PZT | 1 | pzt-d043fc6da2c1 |
| scope-context | Périmètre explicite du Super Admin | 1 | scope-context-20a18bf192a8 |
| scope-context | Tenant racine et parenté unique | 1 | scope-context-49cd4f07132a |
| scope-context | Propriété canonique unique | 1 | scope-context-3a23c52bedfb |
| scope-context | Contexte immuable propagé avant autorisation | 3 | scope-context-a568773185f8 |
| scope-context | Propagation et frontière d'autorisation du ScopeContext | 3 | scope-context-24734273be96 |
| zt-controller | CZT obligatoire et périmètre | 1 | zt-controller-0075d78b8361 |
| zt-controller | Base propre chiffrée et initialisation | 1 | zt-controller-99c13d6319c5 |
| zt-controller | Durabilité synchrone et promotion | 1 | zt-controller-a3a1fca8cc08 |
| zt-controller | Continuité bornée sans primaire | 1 | zt-controller-5f13908e4a13 |
| zt-controller | Gestionnaire réseau et propriétaire unique | 1 | zt-controller-a844ba947c3b |
| zt-controller | Backends et protection des échéances | 1 | zt-controller-0b71d7d52f1b |
| zt-controller | Amorçage et opérations multi-rôles | 1 | zt-controller-b3bc36187257 |

### Référence courante pixs-agent-b22610f19af3

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 55. SHA-256 : `b22610f19af36f8cdceb47b8870b54b63aa9302dc8cbfec91bfe059b3a418ae5`.

Scénarios : Deux processus pour une opération.

~~~~text
### Requirement: Unicité des opérations PA multiprocessus

Les processus PA MUST coordonner propriété des ressources, admission, idempotence et résultats durables selon leurs contrats. Leur multiplication MUST NOT dupliquer un effet, créer une identité ou une autorité implicite, ni permettre des mutations concurrentes incompatibles. Les configurations de ressources MUST être gérées par pixs.agent via PZT avec état appliqué vérifié.

#### Scenario: Deux processus pour une opération

- **WHEN** deux processus PA reçoivent une même opération ou des opérations incompatibles sur une ressource
- **THEN** la coordination conserve l'idempotence et la propriété déclarée sans double application ni choix implicite d'autorité
~~~~

### Référence courante pixs-agent-0ed896227fd4

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 108. SHA-256 : `0ed896227fd4520562a556c15ca86d634e059dc29313794ff743d8324201c20b`.

Scénarios : Composition au build et catalogue fermé.

~~~~text
### Requirement: Composition au build et catalogue fermé

Chaque capacité PA MUST déclarer identité, version, propriétaire, contrats, dépendances, configuration, sécurité et permissions selon le modèle de composants. La composition initiale MUST se faire au build ; instructions et mandats MUST sélectionner seulement des opérations déjà livrées. PA MUST NOT télécharger ou charger implicitement du code, évaluer du Python ou ouvrir un shell privilégié à partir d'une instruction réseau.

#### Scenario: Composition au build et catalogue fermé

- **WHEN** une instruction demande une opération absente du catalogue livré
- **THEN** elle est refusée sans téléchargement ou exécution de code arbitraire
~~~~

### Référence courante pixs-agent-1760abaea35a

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 157. SHA-256 : `1760abaea35a64776c3ea6040206e9e97fa3ef074eea5014629b89bcd71e973a`.

Scénarios : Contrat public des instructions et revalidation.

~~~~text
### Requirement: Contrat public des instructions et revalidation

Une instruction MUST identifier émetteur, acteur initial, exécuteur, opération/version, cible, plateforme, tenant/scope, paramètres typés/bornés, mandat, validité, fraîcheur, corrélation et idempotence lorsqu'applicables. PA MUST vérifier ces éléments à l'exécution, y compris après attente ou reprise. Une permission de lecture/surveillance MUST NOT accorder une reconfiguration ; un canal authentifié MUST NOT accorder un droit métier.

#### Scenario: Contrat public des instructions et revalidation

- **WHEN** une instruction admise expire avant son exécution
- **THEN** elle n'est pas exécutée sur la seule base de son admission passée
~~~~

### Référence courante pixs-agent-ff6703508e08

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 175. SHA-256 : `ff6703508e08fae91c497ab9d48d344859dcbb01e261dec40a9f0c8004849dd4`.

Scénarios : Exécution locale et états indéterminés.

~~~~text
### Requirement: Exécution locale et états indéterminés

Chaque opération MUST déclarer préconditions, postconditions, effets, codes stables, caractère rejouable et stratégie d'erreur. Après crash entre effet et persistance du résultat, PA MUST vérifier la postcondition ou demander une intervention autorisée avant réexécution. Simulation, préparation, exécution et confirmation MUST rester distinctes ; une simulation MUST NOT produire de mutation.

#### Scenario: Exécution locale et états indéterminés

- **WHEN** un crash survient après un effet système avant son enregistrement
- **THEN** la reprise distingue l'effet inconnu et évite une réexécution aveugle
~~~~

### Référence courante pixs-agent-4ad8f35c03d3

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 184. SHA-256 : `4ad8f35c03d379f498c31ee1258ee9d1b218e3913266d4cb8670d6b807881e5f`.

Scénarios : Plans sensibles et compensation préautorisée.

~~~~text
### Requirement: Plans sensibles et compensation préautorisée

Une reconfiguration sensible MUST utiliser un plan versionné, borné, autorisé et encore courant, avec confirmation ou assurance renforcée lorsque requise. Une compensation après perte de contrôle MUST rester dans le plan préautorisé, sans restaurer une permission révoquée ni ouvrir un canal hors PZT. Un plan obsolète ou hors mandat MUST NOT être appliqué.

#### Scenario: Plans sensibles et compensation préautorisée

- **WHEN** une modification coupe le canal de contrôle
- **THEN** l'état est diagnostiqué et seule une compensation encore autorisée peut être tentée
~~~~

### Référence courante pixs-agent-314ad93363d9

Source : [pixs-agent](../../specs/pixs-agent/spec.md), ligne 256. SHA-256 : `314ad93363d9d818e5a7f225d32947753df0c11207a678f2676b7c2c3c744daf`.

Scénarios : Audit, confidentialité et exception Super Admin.

~~~~text
### Requirement: Audit, confidentialité et exception Super Admin

PA et PBO MUST appliquer les obligations ordinaires de security, authorization et audit sous réserve de l'exception unique définie par initial-administration. Une requête Super Admin MUST conserver acteur initial et tenant explicitement accordé, sans credentials ou exception transférés à un worker/autre compte. Audit ou contrôle dérogé/non réalisé MUST NOT être présenté comme effectué ; profils structurels et contrats d'exécution MUST rester distincts.

#### Scenario: Audit, confidentialité et exception Super Admin

- **WHEN** le Super Admin utilise une dérogation d'audit dans son tenant accordé
- **THEN** l'audit absent n'est pas revendiqué comme réalisé et aucun autre compte n'hérite de la dérogation
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

### Référence courante zt-controller-0075d78b8361

Source : [zt-controller](../../specs/zt-controller/spec.md), ligne 11. SHA-256 : `0075d78b83619c5def0567a914d7afbf54e7fb7afa52b4345dbe2a80e6bc8b80`.

Scénarios : Nouvelle configuration.

~~~~text
### Requirement: CZT obligatoire et périmètre

Chaque ZT MUST avoir au moins un CZT exécuté par PZT. CZT MUST gérer enrôlement technique, acteurs et organisation ZT, carte réseau, adressage des pairs, distribution des configurations et réconciliation ; PBO MUST conserver administration et supervision par contrats publics.

#### Scenario: Nouvelle configuration

- **WHEN** une politique réseau est administrée depuis PBO
- **THEN** sa référence est conservée par CZT sans écriture directe PBO dans les tables privées.
~~~~

### Référence courante zt-controller-99c13d6319c5

Source : [zt-controller](../../specs/zt-controller/spec.md), ligne 20. SHA-256 : `99c13d6319c59dbbc43992c47acd6cca1d2c2df7f27ece1b9ac68a44f840dc2a`.

Scénarios : Ajout de CZT.

~~~~text
### Requirement: Base propre chiffrée et initialisation

CZT MUST posséder une PG logique indépendante de PBO, des bases Instance/Domaine, DZT et PKIZT, chiffrée localement. Le premier CZT MUST l'initialiser ; chaque CZT supplémentaire MUST synchroniser sa réplique avec le primaire sans créer de source concurrente.

#### Scenario: Ajout de CZT

- **WHEN** un CZT est ajouté
- **THEN** sa base est synchronisée et vérifiée avant l’autorité correspondante.
~~~~

### Référence courante zt-controller-a3a1fca8cc08

Source : [zt-controller](../../specs/zt-controller/spec.md), ligne 29. SHA-256 : `a3a1fca8cc08c66028525454eb093f5df69735c8571174ce4b9eac4bbd594e0b`.

Scénarios : Réplique requise absente.

~~~~text
### Requirement: Durabilité synchrone et promotion

CZT MUST confirmer l'écriture après persistance sur le primaire et les répliques synchrones requises. Le minimum MUST être configurable sans diminution automatique en cas de panne. La bascule automatique MUST être encadrée, exclure l'ancien primaire, vérifier le candidat et conserver les écritures confirmées.

#### Scenario: Réplique requise absente

- **WHEN** le nombre de confirmations est inférieur au minimum configuré
- **THEN** l’écriture n’est pas confirmée par une réduction automatique du minimum.
~~~~

### Référence courante zt-controller-5f13908e4a13

Source : [zt-controller](../../specs/zt-controller/spec.md), ligne 38. SHA-256 : `5f13908e4a13140cc9c13d07a3e2ba28739ea6998ceb41162998bbdce41205a6`.

Scénarios : Échéance pendant panne.

~~~~text
### Requirement: Continuité bornée sans primaire

Sans CZT primaire opérationnel, les échanges MUST rester limités aux autorisations encore valides et aux révocations connues. Les opérations requérant CZT MUST être suspendues ; un cache MUST NOT émettre ou prolonger de nouveaux droits.

#### Scenario: Échéance pendant panne

- **WHEN** une autorisation expire sans primaire disponible
- **THEN** l’accès cesse sans grâce ni renouvellement local.
~~~~

### Référence courante zt-controller-a844ba947c3b

Source : [zt-controller](../../specs/zt-controller/spec.md), ligne 47. SHA-256 : `a844ba947c3b675f86146904664b15a71a511bff9a7bba354ee3e5e7446cde46`.

Scénarios : Deux rôles demandent des règles.

~~~~text
### Requirement: Gestionnaire réseau et propriétaire unique

Le socle PZT MUST coordonner interfaces, adressage, routage et pare-feu selon les références CZT, en agrégeant les besoins des rôles sous un propriétaire d'écriture par périmètre. Le profil MUST gérer le périmètre PZT par défaut et MAY gérer globalement l'hôte sur choix explicite.

#### Scenario: Deux rôles demandent des règles

- **WHEN** GZT et DZT demandent des règles sur un même périmètre
- **THEN** le gestionnaire commun les réconcilie sans écrivains concurrents ni écrasement hors mandat.
~~~~

### Référence courante zt-controller-0b71d7d52f1b

Source : [zt-controller](../../specs/zt-controller/spec.md), ligne 56. SHA-256 : `0b71d7d52f1b610117e914b3e44b53e11b9824b9ef3da9565f6c8e188849e39d`.

Scénarios : Dérive sans correction autorisée.

~~~~text
### Requirement: Backends et protection des échéances

Les profils MUST qualifier Linux nftables et les capacités demandées iptables/ip6tables/ipset, ainsi que le pare-feu Windows/WFP, sans interchangeabilité présumée. La protection indépendante des autorisations MUST être obligatoire. Configuration déclarative/versionnée/reconstruisible et dérives détectées MUST être distinguées de la correction automatique configurable et désactivée par défaut.

#### Scenario: Dérive sans correction autorisée

- **WHEN** un écart au pare-feu est observé sans politique de réparation
- **THEN** le constat et la mise en sécurité prévue sont rapportés sans correction non autorisée.
~~~~

### Référence courante zt-controller-b3bc36187257

Source : [zt-controller](../../specs/zt-controller/spec.md), ligne 65. SHA-256 : `b3bc3618725797ff4d27c7f5f2d60dd14f808c15d04e1aa0b17a068cc4b6cfd8`.

Scénarios : Réponse perdue.

~~~~text
### Requirement: Amorçage et opérations multi-rôles

L'amorçage technique MUST être limité et borné, distinct du contrôle normal. Une opération multi-rôles MUST posséder un propriétaire unique, un suivi durable et une reprise sans double effet, avec revalidation des mandats et préconditions.

#### Scenario: Réponse perdue

- **WHEN** une étape multi-rôles a pu produire son effet sans réponse
- **THEN** la reprise réconcilie les propriétaires avant répétition.
~~~~
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| pixs-agent / 47 | [Composition au build et catalogue fermé](../../specs/pixs-agent/spec.md#L47) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 92 | [Contrat public des instructions et revalidation](../../specs/pixs-agent/spec.md#L92) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 110 | [Exécution locale et états indéterminés](../../specs/pixs-agent/spec.md#L110) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 119 | [Plans sensibles et compensation préautorisée](../../specs/pixs-agent/spec.md#L119) | ND | CANDIDAT_PROFIL_PA |
| pixs-agent / 182 | [Audit, confidentialité et exception Super Admin](../../specs/pixs-agent/spec.md#L182) | ND | CANDIDAT_PROFIL_PA |
| pzt / 30 | [Passage obligatoire PBO–PA par PZT](../../specs/pzt/spec.md#L30) | ND | APPLICABILITE_ET_DECOUPAGE_A_CONFIRMER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence pixs-agent--bd3940f601

Source : `openspec/specs/pixs-agent/spec.md`, ligne 47. SHA-256 du bloc : `2cde976931df9e6c3f72460dd263b37705129586eb38a9efc3be6b7269446983`.

~~~~text
### Requirement: Composition au build et catalogue fermé

Chaque capacité PA MUST déclarer identité, version, propriétaire, contrats, dépendances, configuration, sécurité et permissions selon le modèle de composants. La composition initiale MUST se faire au build ; instructions et mandats MUST sélectionner seulement des opérations déjà livrées. PA MUST NOT télécharger ou charger implicitement du code, évaluer du Python ou ouvrir un shell privilégié à partir d'une instruction réseau.

#### Scenario: Composition au build et catalogue fermé

- **WHEN** une instruction demande une opération absente du catalogue livré
- **THEN** elle est refusée sans téléchargement ou exécution de code arbitraire
~~~~

### Référence pixs-agent--ab52dc7fd0

Source : `openspec/specs/pixs-agent/spec.md`, ligne 92. SHA-256 du bloc : `bac905dfacb676eca03b3a498b0c86145e43d6273305d3a1cbf6af100037b74e`.

~~~~text
### Requirement: Contrat public des instructions et revalidation

Une instruction MUST identifier émetteur, acteur initial, exécuteur, opération/version, cible, plateforme, tenant/scope, paramètres typés/bornés, mandat, validité, fraîcheur, corrélation et idempotence lorsqu'applicables. PA MUST vérifier ces éléments à l'exécution, y compris après attente ou reprise. Une permission de lecture/surveillance MUST NOT accorder une reconfiguration ; un canal authentifié MUST NOT accorder un droit métier.

#### Scenario: Contrat public des instructions et revalidation

- **WHEN** une instruction admise expire avant son exécution
- **THEN** elle n'est pas exécutée sur la seule base de son admission passée
~~~~

### Référence pixs-agent--13250f4b84

Source : `openspec/specs/pixs-agent/spec.md`, ligne 110. SHA-256 du bloc : `ba23e50b4d683e00934ba0b17353a922954d7198013e34a9c52a41d803a5d47b`.

~~~~text
### Requirement: Exécution locale et états indéterminés

Chaque opération MUST déclarer préconditions, postconditions, effets, codes stables, caractère rejouable et stratégie d'erreur. Après crash entre effet et persistance du résultat, PA MUST vérifier la postcondition ou demander une intervention autorisée avant réexécution. Simulation, préparation, exécution et confirmation MUST rester distinctes ; une simulation MUST NOT produire de mutation.

#### Scenario: Exécution locale et états indéterminés

- **WHEN** un crash survient après un effet système avant son enregistrement
- **THEN** la reprise distingue l'effet inconnu et évite une réexécution aveugle
~~~~

### Référence pixs-agent--df000cdcc2

Source : `openspec/specs/pixs-agent/spec.md`, ligne 119. SHA-256 du bloc : `e143fe2bc291943350997951ca533d1ccbe2ac1c370072914daaf5f915b3c4fc`.

~~~~text
### Requirement: Plans sensibles et compensation préautorisée

Une reconfiguration sensible MUST utiliser un plan versionné, borné, autorisé et encore courant, avec confirmation ou assurance renforcée lorsque requise. Une compensation après perte de contrôle MUST rester dans le plan préautorisé, sans restaurer une permission révoquée ni ouvrir un canal hors PZT. Un plan obsolète ou hors mandat MUST NOT être appliqué.

#### Scenario: Plans sensibles et compensation préautorisée

- **WHEN** une modification coupe le canal de contrôle
- **THEN** l'état est diagnostiqué et seule une compensation encore autorisée peut être tentée
~~~~

### Référence pixs-agent--8680fa3b61

Source : `openspec/specs/pixs-agent/spec.md`, ligne 182. SHA-256 du bloc : `b9d9011f0a6a37e20b1d9e49627c3c8289fd325c3b015054f91e78ccf530f22a`.

~~~~text
### Requirement: Audit, confidentialité et exception Super Admin

PA et PBO MUST appliquer les obligations ordinaires de security, authorization et audit sous réserve de l'exception unique définie par initial-administration. Une requête Super Admin MUST conserver acteur initial et tenant explicitement accordé, sans credentials ou exception transférés à un worker/autre compte. Audit ou contrôle dérogé/non réalisé MUST NOT être présenté comme effectué ; profils structurels et contrats d'exécution MUST rester distincts.

#### Scenario: Audit, confidentialité et exception Super Admin

- **WHEN** le Super Admin utilise une dérogation d'audit dans son tenant accordé
- **THEN** l'audit absent n'est pas revendiqué comme réalisé et aucun autre compte n'hérite de la dérogation
~~~~

### Référence pzt--b09abd6f60

Source : `openspec/specs/pzt/spec.md`, ligne 30. SHA-256 du bloc : `efd3979f85e17ba446c232d0fd897c0c83be33aca423a3668342e3a8a822481d`.

~~~~text
### Requirement: Passage obligatoire PBO–PA par PZT

Tous les échanges PBO–PA, instructions, configuration, administration, états, diagnostics, événements et résultats MUST passer par PZT dans les deux sens, même sur le même hôte ou conteneur. Le transport local mTLS MUST conserver identification, autorisation, chiffrement, validité, anti-rejeu et traçabilité ; WireGuard local n'est pas obligatoire. Un profil local indisponible MUST NOT déclencher un canal Unix, loopback ou fichier de substitution hors PZT.

#### Scenario: Passage obligatoire PBO–PA par PZT

- **WHEN** le transport local PZT n'est pas vérifiable
- **THEN** le contrôle PBO–PA concerné est bloqué sans repli de proximité
~~~~

