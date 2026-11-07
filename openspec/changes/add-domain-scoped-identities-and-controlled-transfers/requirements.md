# Références normatives — C96

Plan ACL-PIXS-2026-10-31-E3-R1, validé ; relevé du 31 octobre 2026. Les blocs ci-dessous sont des copies de référence, jamais des deltas ADDED/MODIFIED ni une autorité indépendante du canon. Leur présence ne prouve aucune réalisation.

## Traçabilité des exigences et scénarios

| Capacité | Exigence cible | Scénarios | Référence |
|---|---|---:|---|
| core | Module obligatoire au-dessus du noyau | 1 | core-fc5c17b85882 |
| core | Primitives minimales communes | 1 | core-a15db0a0e874 |
| core | Aucun fournisseur concret imposé | 1 | core-71fb8ebb9b15 |
| core | Profil minimal des utilisateurs et identités numériques v1 | 2 | core-cad742eb1a6c |
| core | Liaison utilisateur identité explicite et unique | 2 | core-5be4341f9029 |
| core | Représentation minimale des comptes de service | 1 | core-1ec1c0295927 |
| core | Frontière des validateurs du profil identité | 1 | core-9641b83b4301 |
| core | Autorités et limites du profil identité structurel | 1 | core-0b6602b1da05 |
| core | Frontière Core Auth et dépendance unidirectionnelle | 1 | core-fe32af48f650 |
| core | Moyens multiples sans multiplication implicite des identités | 1 | core-7d3a8ec34441 |
| core | Évolution versionnée du lien individu identités | 1 | core-810ca819ba83 |
| scope-context | Périmètre explicite du Super Admin | 1 | scope-context-20a18bf192a8 |
| scope-context | Tenant racine et parenté unique | 1 | scope-context-49cd4f07132a |
| scope-context | Propriété canonique unique | 1 | scope-context-3a23c52bedfb |
| scope-context | Contexte immuable propagé avant autorisation | 3 | scope-context-a568773185f8 |
| scope-context | Propagation et frontière d'autorisation du ScopeContext | 3 | scope-context-24734273be96 |
| pixs-domains | Tenants et propriété des ressources | 2 | pixs-domains-784b3416b755 |
| pixs-domains | Individus et identités multiples | 1 | pixs-domains-8e5157150f7c |
| pixs-domains | Transferts fonctionnels contrôlés V1 | 1 | pixs-domains-ba4dfa97bf7d |
| pixs-domains | Structures organisationnelles non transférables V1 | 1 | pixs-domains-2d4b91559aa3 |
| pixs-domains | Retrait du premier Domaine | 1 | pixs-domains-f9d0dad1d882 |
| pixs-instance | Références PG avant et après Domaine | 1 | pixs-instance-9baefb0c5ae7 |
| pixs-instance | Administration globale par identités habilitées | 1 | pixs-instance-8c964dc84f92 |
| pixs-instance | Habilitations Instance et domaines | 1 | pixs-instance-b7a2b5d23968 |

## Blocs sources complets

### Référence core-fc5c17b85882

Source : [core](../../specs/core/spec.md), ligne 8. SHA-256 du bloc : `fc5c17b85882a8ba45a10882c27301127360d7d338acfed61ae555f474e99776`.

Scénarios sources : Composition sans core refusée.

~~~~text
### Requirement: Module obligatoire au-dessus du noyau

Toute composition Pixs MUST inclure pixs.core comme module requis ; une composition sans pixs.core est invalide.

#### Scenario: Composition sans core refusée

- **WHEN** une composition omet pixs.core
- **THEN** l'activation est refusée avant tout chargement
~~~~

### Référence core-a15db0a0e874

Source : [core](../../specs/core/spec.md), ligne 17. SHA-256 du bloc : `a15db0a0e874b998aae0d3883b0347bb0489c0e07ef375e39225258e613241f9`.

Scénarios sources : Primitive consommée par contrat.

~~~~text
### Requirement: Primitives minimales communes

pixs.core MUST exposer individus, identités numériques, groupes, appartenances, tenants, rôles, ACL et permissions via contrats publics. Le référentiel d'individus MUST être commun à l'Instance. PG Instance/Domaine MUST conserver leur vérité selon pixs-instance ; la publication LDAP MUST suivre directory-projections et auth-managed-directory sans remplacer PG.

#### Scenario: Primitive consommée par contrat

- **WHEN** un module demande une identité ou une appartenance
- **THEN** il utilise le contrat propriétaire sans accès direct aux tables privées.
~~~~

### Référence core-71fb8ebb9b15

Source : [core](../../specs/core/spec.md), ligne 26. SHA-256 du bloc : `71fb8ebb9b15814ee30b4a4c0ce5c9bb1ddb832abf1cc4559300abf76d76eeb6`.

Scénarios sources : Fournisseur compatible.

~~~~text
### Requirement: Aucun fournisseur concret imposé

Le noyau et les contrats génériques Core MUST rester agnostiques des implémentations. Les profils MUST déclarer leurs fournisseurs requis, dont PG source Core et OpenLDAP/MIT Kerberos en mode Domaine, sans intégrer leur code au noyau ni activer implicitement un service.

#### Scenario: Fournisseur compatible

- **WHEN** un fournisseur compatible est sélectionné dans les limites du profil
- **THEN** les consommateurs gardent leurs contrats sans dépendre de son implémentation privée.
~~~~

### Référence core-cad742eb1a6c

Source : [core](../../specs/core/spec.md), ligne 35. SHA-256 du bloc : `cad742eb1a6c4eb163ea45410ed7ee9c86448a3e4be1a3f079032d8fe403f16d`.

Scénarios sources : Identité minimale valide; Identifiant ou vocabulaire invalide.

~~~~text
### Requirement: Profil minimal des utilisateurs et identités numériques v1

Les identifiants internes stables de `User` et `DigitalIdentity` MUST être
des UUIDv7. Le profil v1 de `DigitalIdentity` MUST porter un type explicite
parmi `HUMAN`, `SERVICE`, `DEVICE` et `FEDERATED`, et un état explicite
parmi `ACTIVE`, `SUSPENDED`, `REVOKED` et `EXPIRED`. Les validateurs
MUST rejeter un identifiant non UUIDv7, un type inconnu ou un état inconnu ;
ils MUST NOT déduire un état, un type ou une assurance d'un provider.

#### Scenario: Identité minimale valide

- **WHEN** un utilisateur et une identité HUMAN à l'état ACTIVE portent chacun un UUIDv7 valide
- **THEN** leurs représentations minimales sont acceptées sans exiger une authentification ou une liaison entre eux

#### Scenario: Identifiant ou vocabulaire invalide

- **WHEN** un identifiant n'est pas un UUIDv7 ou le type ou l'état n'appartient pas au vocabulaire fermé du profil v1
- **THEN** la validation refuse la représentation concernée
~~~~

### Référence core-5be4341f9029

Source : [core](../../specs/core/spec.md), ligne 54. SHA-256 du bloc : `5be4341f90297f703e132f31ac54e36f7b95b9eeee07f1115391e4b32f8fce64`.

Scénarios sources : Plusieurs identités du même individu; Identité liée à deux individus.

~~~~text
### Requirement: Liaison utilisateur identité explicite et unique

Un individu User MUST pouvoir exister sans DigitalIdentity et une identité technique MUST pouvoir exister sans individu. Chaque identité MUST être liée à au plus un individu ; un individu MUST pouvoir posséder plusieurs identités par Domaine selon pixs-domains. Les références MUST être existantes, explicites et cohérentes avec leur périmètre ; elles MUST NOT être déduites d'un nom, email ou identifiant externe.

#### Scenario: Plusieurs identités du même individu

- **WHEN** un individu possède une identité courante et une identité administrative dans le même Domaine
- **THEN** les deux liaisons sont admises avec profils et droits distincts.

#### Scenario: Identité liée à deux individus

- **WHEN** la même identité est liée à deux individus ou à une référence absente
- **THEN** la liaison est refusée.
~~~~

### Référence core-1ec1c0295927

Source : [core](../../specs/core/spec.md), ligne 68. SHA-256 du bloc : `1ec1c0295927e8168d6acb338b99c9f7f50340b776ac6c536f89a61c164fde51`.

Scénarios sources : Compte de service sans utilisateur.

~~~~text
### Requirement: Représentation minimale des comptes de service

Dans le profil v1, un compte de service MUST être représenté par une
`DigitalIdentity` de type `SERVICE`. Cette représentation MUST pouvoir
exister sans utilisateur lié et MUST NOT conférer par elle-même de droit
d'accès ni de niveau d'assurance.

#### Scenario: Compte de service sans utilisateur

- **WHEN** une identité SERVICE possède un UUIDv7 et un état valides sans utilisateur lié
- **THEN** sa représentation de compte de service est acceptée sans établir une authentification ni une autorisation
~~~~

### Référence core-9641b83b4301

Source : [core](../../specs/core/spec.md), ligne 80. SHA-256 du bloc : `9641b83b4301530600349bf2b779a1cd8a2a59ab86a38aa7588ecea6a9c5f4f0`.

Scénarios sources : Validation structurelle sans effet applicatif.

~~~~text
### Requirement: Frontière des validateurs du profil identité

La validation structurelle du profil v1 MUST pouvoir être exercée sur des
modèles sans authentification réelle, provider concret ni persistance. Elle MUST NOT être présentée comme une authentification, une autorisation,
une mutation persistante ou une preuve d'audit durable.

#### Scenario: Validation structurelle sans effet applicatif

- **WHEN** un modèle d'identité satisfait le profil structurel
- **THEN** cette validation ne crée aucune session, ne persiste aucune entité et n'accorde aucun accès
~~~~

### Référence core-0b6602b1da05

Source : [core](../../specs/core/spec.md), ligne 91. SHA-256 du bloc : `0b6602b1da05f941115747a0bdac11582bcc6db4d887493bf0dd87144a80674b`.

Scénarios sources : Identité structurelle sans assurance implicite.

~~~~text
### Requirement: Autorités et limites du profil identité structurel

Le backend Django
MUST rester l'autorité métier et transactionnelle ; PostgreSQL MUST rester
la source de vérité applicative. Les mutations réelles MUST conserver les
exigences applicables de persistance, d'autorisation et d'audit. Le profil structurel MUST NOT définir implicitement des transitions d'état,
des règles temporelles ou des niveaux d'assurance à partir du seul type
ou état de l'identité.

#### Scenario: Identité structurelle sans assurance implicite

- **WHEN** un modèle satisfait le profil structurel d'identité
- **THEN** son type ou son état ne définit pas implicitement de transition, règle temporelle ou niveau d'assurance, et les mutations restent sous l'autorité backend
~~~~

### Référence core-fe32af48f650

Source : [core](../../specs/core/spec.md), ligne 105. SHA-256 du bloc : `fe32af48f650fc38400dc2d1f8a081762b649f6c3cbc693b8a33d669fd95e370`.

Scénarios sources : Révocation canonique.

~~~~text
### Requirement: Frontière Core Auth et dépendance unidirectionnelle

pixs.core MUST rester propriétaire de User, DigitalIdentity, liens, groupes, appartenances, tenants, rôles, ACL et permissions. pixs.auth MUST consommer ses contrats publics pour ces données. Core MUST NOT dépendre d'une implémentation Auth ni héberger ses protocoles, sessions ou secrets. Les contrats purs partagés existants MUST rester réutilisables sans déplacement imposé.

#### Scenario: Révocation canonique
- **WHEN** Core confirme la révocation d'une DigitalIdentity
- **THEN** Auth invalide les accès concernés selon son contrat sans écriture Core dans une table privée Auth ni cycle de dépendances
~~~~

### Référence core-7d3a8ec34441

Source : [core](../../specs/core/spec.md), ligne 113. SHA-256 du bloc : `7d3a8ec344411de2b477f833bcfefc4790f600c535142cce6aaedbbed958e266`.

Scénarios sources : Passkey et principal pour une identité.

~~~~text
### Requirement: Moyens multiples sans multiplication implicite des identités

Une DigitalIdentity MUST pouvoir avoir plusieurs moyens et sources sous propriété Auth. Ajouter une méthode MUST NOT créer une identité, une appartenance ou un droit implicite. La cardinalité des identités par individu MUST suivre la liaison explicite ci-dessus, sans fusion d'identités distinctes par partage d'un moyen ou nom.

#### Scenario: Passkey et principal pour une identité

- **WHEN** une passkey et un principal Kerberos sont liés à une identité
- **THEN** son UUID et ses habilitations restent inchangés sans compte supplémentaire.
~~~~

### Référence core-810ca819ba83

Source : [core](../../specs/core/spec.md), ligne 123. SHA-256 du bloc : `810ca819ba83be9240790e2382bfa67eb864a7839821bd925e3ca212adaa0f80`.

Scénarios sources : Contrat v1 existant.

~~~~text
### Requirement: Évolution versionnée du lien individu identités

Les contrats et modèles v1 MUST conserver leurs références de preuve et être distingués du modèle à plusieurs identités par individu et Domaine. Le nouveau modèle MUST suivre une évolution versionnée et des migrations préservant identités et relations ; une ancienne recette v1 MUST NOT qualifier automatiquement le nouveau lien.

#### Scenario: Contrat v1 existant

- **WHEN** un modèle validé pour la liaison unique v1 est examiné
- **THEN** sa preuve reste bornée à cette version et ne démontre pas la nouvelle cardinalité Domaine
~~~~

### Référence scope-context-20a18bf192a8

Source : [scope-context](../../specs/scope-context/spec.md), ligne 8. SHA-256 du bloc : `20a18bf192a8b52d7e7a3ae6628f6b82dea2833869a146235d4f667c9725c213`.

Scénarios sources : Accord tenant sans changement de propriété.

~~~~text
### Requirement: Périmètre explicite du Super Admin

L'exception Super Admin MUST suivre `authorization` sans modifier la structure du ScopeContext ni la propriété canonique des ressources. Le contrôle total tenant-scoped MUST exiger un accord explicite préalable pour le tenant concerné. Les exigences d'audit de périmètre MUST rester dérogeables pour ce seul compte selon `audit`.

#### Scenario: Accord tenant sans changement de propriété

- **WHEN** le Super Admin reçoit un accès explicite au tenant A puis agit malgré une ACL de A
- **THEN** le ScopeContext reste TENANT avec le tenant A et la ressource conserve sa propriété canonique
- **AND** un tenant B non accordé reste hors de son périmètre
~~~~

### Référence scope-context-49cd4f07132a

Source : [scope-context](../../specs/scope-context/spec.md), ligne 18. SHA-256 du bloc : `49cd4f07132ad31022e1f642726b4a08752a7abd67a12d9933e2b3c0308d15c9`.

Scénarios sources : Cycle de scopes refusé.

~~~~text
### Requirement: Tenant racine et parenté unique

Chaque tenant MUST rester la racine de ses scopes enfants ; chaque scope enfant MUST avoir un parent unique dans ce tenant sans cycle. En mode Domaine, chaque tenant MUST appartenir à un seul Domaine selon pixs-domains. Les périmètres Instance et Domaine MUST rester distincts de la hiérarchie interne des scopes tenant.

#### Scenario: Cycle de scopes refusé

- **WHEN** une parenté crée un cycle ou rattache un scope à un autre tenant
- **THEN** la déclaration est refusée avant activation.
~~~~

### Référence scope-context-3a23c52bedfb

Source : [scope-context](../../specs/scope-context/spec.md), ligne 27. SHA-256 du bloc : `3a23c52bedfbfa5d0ae6a079534b9a15da12cd0b14ebc79d7a89147247978542`.

Scénarios sources : Scope sans tenant cohérent refusé.

~~~~text
### Requirement: Propriété canonique unique

Chaque ressource MUST avoir une propriété canonique unique : Instance, Domaine, Tenant ou scope enfant cohérent. En mode Domaine, un tenant propriétaire MUST référencer son Domaine. Partage, délégation et ACL MUST NOT changer cette propriété ou permettre un accès implicite. Les références historiques PLATFORM MUST être distinguées du nouveau contexte versionné.

#### Scenario: Scope sans tenant cohérent refusé

- **WHEN** un scope propriétaire ne correspond pas au tenant déclaré
- **THEN** la mutation est refusée sans accès à un autre périmètre.
~~~~

### Référence scope-context-a568773185f8

Source : [scope-context](../../specs/scope-context/spec.md), ligne 36. SHA-256 du bloc : `a568773185f8eea21b482e1bf41a3c33896e6fad732c43e8eb93d16f8763ed93`.

Scénarios sources : Contexte TENANT sans tenant refusé; Contexte PLATFORM avec identifiants refusé; Nouveau parcours Domaine sur contexte incomplet.

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

### Référence scope-context-24734273be96

Source : [scope-context](../../specs/scope-context/spec.md), ligne 55. SHA-256 du bloc : `24734273be961e63f77378a58b4027d3469843b00bada4ee705920c8aeb51557`.

Scénarios sources : Élargissement implicite refusé; Contexte PLATFORM sans identifiants accepté sans octroyer permission; Accès plateforme sans permission refusé et audité.

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

### Référence pixs-domains-784b3416b755

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 52. SHA-256 du bloc : `784b3416b7559266c7a1b38d15a475ebd8b05a90e2f00eb976a8bf198703e0f4`.

Scénarios sources : Domaine sans tenant; Tenant rattaché deux fois.

~~~~text
### Requirement: Tenants et propriété des ressources

Un Domaine MUST accepter zéro, un ou plusieurs tenants ; chaque tenant MUST appartenir à un seul Domaine après transition. Les scopes enfants MUST rester rattachés à leur tenant sans cycles. Les propriétés Instance, Domaine et Tenant MUST être distinctes et n'accorder aucun droit implicite.

#### Scenario: Domaine sans tenant

- **WHEN** un Domaine opérationnel ne contient aucun tenant
- **THEN** ses services et son rattachement ZT restent valides.

#### Scenario: Tenant rattaché deux fois

- **WHEN** une mutation rattache simultanément un tenant à deux Domaines
- **THEN** elle est refusée sans ambiguïté de propriétaire.
~~~~

### Référence pixs-domains-8e5157150f7c

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 66. SHA-256 du bloc : `8e5157150f7c0a1801085b1c19bdd9c69fe4c345dcba246bb25ed2aba4727793`.

Scénarios sources : Affiliation sans admission.

~~~~text
### Requirement: Individus et identités multiples

Un individu Core MUST pouvoir être affilié à plusieurs Domaines et tenants et posséder plusieurs identités par Domaine. Chaque participation MUST conserver ses admissions, profils et habilitations. Une affiliation Core MUST NOT valoir admission ZT, sauf politique automatique explicite.

#### Scenario: Affiliation sans admission

- **WHEN** un individu est affilié à Recherche sans politique d’admission automatique
- **THEN** son appartenance ZT n’est pas créée par cette seule affiliation.
~~~~

### Référence pixs-domains-ba4dfa97bf7d

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 75. SHA-256 du bloc : `ba4dfa97bf7dfe8389d5a8f4597671aa9630b9e24d13f8a2ea071bc82dc36b12`.

Scénarios sources : Tenant transféré.

~~~~text
### Requirement: Transferts fonctionnels contrôlés V1

La V1 MUST prévoir les transferts autorisés d'identités numériques, données métier et tenants entre Domaines de la même Instance, avec vérification des dépendances, continuité des références et réévaluation des droits cibles. Le transfert MUST NOT copier implicitement des autorisations ni être présenté comme déplacement d'une brique exécutable.

#### Scenario: Tenant transféré

- **WHEN** un transfert de tenant est engagé entre deux Domaines
- **THEN** son identité est conservée, son propriétaire est unique et les habilitations de destination sont réévaluées.
~~~~

### Référence pixs-domains-2d4b91559aa3

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 84. SHA-256 du bloc : `2d4b91559aa387da2cb8be333d66674748a755850567e45bba8b742811112985`.

Scénarios sources : Transfert de département.

~~~~text
### Requirement: Structures organisationnelles non transférables V1

La V1 MUST NOT proposer le transfert fonctionnel de structures organisationnelles entre Domaines. Miroitage autorisé et réorganisation interne MUST rester distincts d'un tel transfert.

#### Scenario: Transfert de département

- **WHEN** une demande V1 vise à transférer un département entre Domaines
- **THEN** elle est refusée comme hors périmètre sans modifier les structures source ou cible.
~~~~

### Référence pixs-domains-f9d0dad1d882

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 93. SHA-256 du bloc : `f9d0dad1d882e815cf4d5b665b2037e6591dcb271ed3dd1e9f7605fcd4759334`.

Scénarios sources : Dernier Domaine.

~~~~text
### Requirement: Retrait du premier Domaine

Le premier Domaine MAY être retiré par procédure explicite si au moins un autre Domaine est opérationnel et si données, identités, authentification globale et dépendances sont traitées. Le retrait MUST NOT rétablir Standalone, laisser l'administration sans identité admissible ou retirer un ZT partagé encore requis.

#### Scenario: Dernier Domaine

- **WHEN** le retrait vise le seul Domaine opérationnel
- **THEN** il est refusé sans retour implicite en Standalone.
~~~~

### Référence pixs-instance-9baefb0c5ae7

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 57. SHA-256 du bloc : `9baefb0c5ae783cb168944c78c34b6f7bc7814b244f9c8888e21389eef0e6e37`.

Scénarios sources : Activation du premier Domaine.

~~~~text
### Requirement: Références PG avant et après Domaine

Avant le premier Domaine, PG Instance MUST porter individus, identités numériques, organigrammes Core, groupes, ACL et données métier pré-domaine. Après activation, PG Instance MUST conserver les individus et données communes sans identité numérique d'Instance ; les identités et données reprises MUST appartenir à PG du premier Domaine, avec identifiants et relations préservés.

#### Scenario: Activation du premier Domaine

- **WHEN** le transfert pré-domaine est confirmé
- **THEN** l’identité de Domaine devient utilisable selon son profil et l’ancienne identité d’Instance ne reste pas une autre voie de connexion.
~~~~

### Référence pixs-instance-8c964dc84f92

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 75. SHA-256 du bloc : `8c964dc84f92c940b5c3ba094d124ffaeb003db84c0f5617cc9487e8d70c38e3`.

Scénarios sources : Domaine d’authentification non habilité.

~~~~text
### Requirement: Administration globale par identités habilitées

Après activation du premier Domaine, l'administration globale MUST utiliser des identités de Domaines explicitement habilitées. Plusieurs Domaines d'authentification MAY être autorisés. Une panne LDAP/Kerberos MAY être traitée par un profil PG Domaine explicitement autorisé et qualifié ; elle MUST NOT recréer d'identité numérique d'Instance ni réduire l'assurance exigée.

#### Scenario: Domaine d’authentification non habilité

- **WHEN** un utilisateur authentifié par un Domaine non habilité demande l’administration globale
- **THEN** la demande est refusée malgré la validité de son authentification.
~~~~

### Référence pixs-instance-b7a2b5d23968

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 93. SHA-256 du bloc : `b7a2b5d2396839fee82af4ccc545e2c2c542dcbef6458888992a032fce8e929f`.

Scénarios sources : PBO mutualisé.

~~~~text
### Requirement: Habilitations Instance et domaines

Les habilitations globales Instance et celles de chaque Domaine MUST être séparées et vérifiées. Le partage d'un PBO, PA, stockage physique ou réseau MUST NOT les transmettre implicitement.

#### Scenario: PBO mutualisé

- **WHEN** un administrateur d’un Domaine utilise un PBO servant plusieurs Domaines
- **THEN** son action reste limitée aux périmètres explicitement autorisés.
~~~~
