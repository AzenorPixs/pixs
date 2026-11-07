# Références normatives — add-auth-identity-enrollment

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Références courantes du périmètre validé

Les copies plus anciennes conservées dans ce fichier sont historiques. Seuls les blocs ci-dessous correspondent au référentiel de la cible consolidée. Ils ne sont pas des deltas à synchroniser et ne prouvent aucune implémentation.

| Capacité | Exigence | Scénarios | Référence |
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
| pixs-domains | Identité et FQDN explicites | 1 | pixs-domains-02f0f83aed5e |
| pixs-domains | ZT obligatoire dédié ou partagé | 2 | pixs-domains-686f4e13ff70 |
| pixs-domains | Isolation dans un ZT partagé | 1 | pixs-domains-bd2991264b73 |
| pixs-domains | Services minimaux par Domaine | 1 | pixs-domains-c9ce061e2b23 |
| pixs-domains | Tenants et propriété des ressources | 2 | pixs-domains-784b3416b755 |
| pixs-domains | Individus et identités multiples | 1 | pixs-domains-8e5157150f7c |
| pixs-domains | Transferts fonctionnels contrôlés V1 | 1 | pixs-domains-ba4dfa97bf7d |
| pixs-domains | Structures organisationnelles non transférables V1 | 1 | pixs-domains-2d4b91559aa3 |
| pixs-domains | Retrait du premier Domaine | 1 | pixs-domains-f9d0dad1d882 |
| pixs-domains | Approbations internes et externes | 1 | pixs-domains-94814997f512 |
| pixs-domains | Références PG et services de Domaine en mode normal ou critique | 1 | pixs-domains-d8fce09ab784 |
| zt-instances | Acteurs et identité persistante | 1 | zt-instances-8b936c8ce6e3 |
| zt-instances | Appartenances selon la catégorie | 1 | zt-instances-02f45c3fc9a4 |
| zt-instances | Gouvernance commune et délégations | 1 | zt-instances-6518a8a762d8 |
| zt-instances | Admission administrative et préautorisation | 1 | zt-instances-fe908c4cf04e |
| zt-instances | Participations permanentes et temporaires | 1 | zt-instances-b0acd891069f |
| zt-instances | Approbations directionnelles et bornées | 1 | zt-instances-abd1a7f7a384 |
| zt-instances | Politiques durables et autorisations bornées | 1 | zt-instances-b9367d6d6b27 |
| zt-instances | Appartenance et preuve sans permission implicite | 1 | zt-instances-cc529473dd70 |
| zt-instances | Représentation explicite et indépendante | 1 | zt-instances-4208f537345f |
| zt-instances | Mandats et session | 1 | zt-instances-906ddd8e7c4a |
| zt-instances | Propagation des états autoritatifs | 1 | zt-instances-9e1b32b3ada0 |
| zt-instances | Socle et minima opérationnels ZT | 1 | zt-instances-e45def8cb779 |
| zt-instances | Existence et disponibilité distinctes | 1 | zt-instances-b6e16e2c94a8 |
| zt-instances | Sortie et révocation séparées | 1 | zt-instances-a979db4ef59b |

### Référence courante core-fc5c17b85882

Source : [core](../../specs/core/spec.md), ligne 8. SHA-256 : `fc5c17b85882a8ba45a10882c27301127360d7d338acfed61ae555f474e99776`.

Scénarios : Composition sans core refusée.

~~~~text
### Requirement: Module obligatoire au-dessus du noyau

Toute composition Pixs MUST inclure pixs.core comme module requis ; une composition sans pixs.core est invalide.

#### Scenario: Composition sans core refusée

- **WHEN** une composition omet pixs.core
- **THEN** l'activation est refusée avant tout chargement
~~~~

### Référence courante core-a15db0a0e874

Source : [core](../../specs/core/spec.md), ligne 17. SHA-256 : `a15db0a0e874b998aae0d3883b0347bb0489c0e07ef375e39225258e613241f9`.

Scénarios : Primitive consommée par contrat.

~~~~text
### Requirement: Primitives minimales communes

pixs.core MUST exposer individus, identités numériques, groupes, appartenances, tenants, rôles, ACL et permissions via contrats publics. Le référentiel d'individus MUST être commun à l'Instance. PG Instance/Domaine MUST conserver leur vérité selon pixs-instance ; la publication LDAP MUST suivre directory-projections et auth-managed-directory sans remplacer PG.

#### Scenario: Primitive consommée par contrat

- **WHEN** un module demande une identité ou une appartenance
- **THEN** il utilise le contrat propriétaire sans accès direct aux tables privées.
~~~~

### Référence courante core-71fb8ebb9b15

Source : [core](../../specs/core/spec.md), ligne 26. SHA-256 : `71fb8ebb9b15814ee30b4a4c0ce5c9bb1ddb832abf1cc4559300abf76d76eeb6`.

Scénarios : Fournisseur compatible.

~~~~text
### Requirement: Aucun fournisseur concret imposé

Le noyau et les contrats génériques Core MUST rester agnostiques des implémentations. Les profils MUST déclarer leurs fournisseurs requis, dont PG source Core et OpenLDAP/MIT Kerberos en mode Domaine, sans intégrer leur code au noyau ni activer implicitement un service.

#### Scenario: Fournisseur compatible

- **WHEN** un fournisseur compatible est sélectionné dans les limites du profil
- **THEN** les consommateurs gardent leurs contrats sans dépendre de son implémentation privée.
~~~~

### Référence courante core-cad742eb1a6c

Source : [core](../../specs/core/spec.md), ligne 35. SHA-256 : `cad742eb1a6c4eb163ea45410ed7ee9c86448a3e4be1a3f079032d8fe403f16d`.

Scénarios : Identité minimale valide; Identifiant ou vocabulaire invalide.

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

### Référence courante core-5be4341f9029

Source : [core](../../specs/core/spec.md), ligne 54. SHA-256 : `5be4341f90297f703e132f31ac54e36f7b95b9eeee07f1115391e4b32f8fce64`.

Scénarios : Plusieurs identités du même individu; Identité liée à deux individus.

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

### Référence courante core-1ec1c0295927

Source : [core](../../specs/core/spec.md), ligne 68. SHA-256 : `1ec1c0295927e8168d6acb338b99c9f7f50340b776ac6c536f89a61c164fde51`.

Scénarios : Compte de service sans utilisateur.

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

### Référence courante core-9641b83b4301

Source : [core](../../specs/core/spec.md), ligne 80. SHA-256 : `9641b83b4301530600349bf2b779a1cd8a2a59ab86a38aa7588ecea6a9c5f4f0`.

Scénarios : Validation structurelle sans effet applicatif.

~~~~text
### Requirement: Frontière des validateurs du profil identité

La validation structurelle du profil v1 MUST pouvoir être exercée sur des
modèles sans authentification réelle, provider concret ni persistance. Elle MUST NOT être présentée comme une authentification, une autorisation,
une mutation persistante ou une preuve d'audit durable.

#### Scenario: Validation structurelle sans effet applicatif

- **WHEN** un modèle d'identité satisfait le profil structurel
- **THEN** cette validation ne crée aucune session, ne persiste aucune entité et n'accorde aucun accès
~~~~

### Référence courante core-0b6602b1da05

Source : [core](../../specs/core/spec.md), ligne 91. SHA-256 : `0b6602b1da05f941115747a0bdac11582bcc6db4d887493bf0dd87144a80674b`.

Scénarios : Identité structurelle sans assurance implicite.

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

### Référence courante core-fe32af48f650

Source : [core](../../specs/core/spec.md), ligne 105. SHA-256 : `fe32af48f650fc38400dc2d1f8a081762b649f6c3cbc693b8a33d669fd95e370`.

Scénarios : Révocation canonique.

~~~~text
### Requirement: Frontière Core Auth et dépendance unidirectionnelle

pixs.core MUST rester propriétaire de User, DigitalIdentity, liens, groupes, appartenances, tenants, rôles, ACL et permissions. pixs.auth MUST consommer ses contrats publics pour ces données. Core MUST NOT dépendre d'une implémentation Auth ni héberger ses protocoles, sessions ou secrets. Les contrats purs partagés existants MUST rester réutilisables sans déplacement imposé.

#### Scenario: Révocation canonique
- **WHEN** Core confirme la révocation d'une DigitalIdentity
- **THEN** Auth invalide les accès concernés selon son contrat sans écriture Core dans une table privée Auth ni cycle de dépendances
~~~~

### Référence courante core-7d3a8ec34441

Source : [core](../../specs/core/spec.md), ligne 113. SHA-256 : `7d3a8ec344411de2b477f833bcfefc4790f600c535142cce6aaedbbed958e266`.

Scénarios : Passkey et principal pour une identité.

~~~~text
### Requirement: Moyens multiples sans multiplication implicite des identités

Une DigitalIdentity MUST pouvoir avoir plusieurs moyens et sources sous propriété Auth. Ajouter une méthode MUST NOT créer une identité, une appartenance ou un droit implicite. La cardinalité des identités par individu MUST suivre la liaison explicite ci-dessus, sans fusion d'identités distinctes par partage d'un moyen ou nom.

#### Scenario: Passkey et principal pour une identité

- **WHEN** une passkey et un principal Kerberos sont liés à une identité
- **THEN** son UUID et ses habilitations restent inchangés sans compte supplémentaire.
~~~~

### Référence courante core-810ca819ba83

Source : [core](../../specs/core/spec.md), ligne 123. SHA-256 : `810ca819ba83be9240790e2382bfa67eb864a7839821bd925e3ca212adaa0f80`.

Scénarios : Contrat v1 existant.

~~~~text
### Requirement: Évolution versionnée du lien individu identités

Les contrats et modèles v1 MUST conserver leurs références de preuve et être distingués du modèle à plusieurs identités par individu et Domaine. Le nouveau modèle MUST suivre une évolution versionnée et des migrations préservant identités et relations ; une ancienne recette v1 MUST NOT qualifier automatiquement le nouveau lien.

#### Scenario: Contrat v1 existant

- **WHEN** un modèle validé pour la liaison unique v1 est examiné
- **THEN** sa preuve reste bornée à cette version et ne démontre pas la nouvelle cardinalité Domaine
~~~~

### Référence courante pixs-domains-02f0f83aed5e

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 11. SHA-256 : `02f0f83aed5e7e038716c3f91cc0b8f31edb2c5ea812cd6dbe8b37b700589e39`.

Scénarios : Racine déjà utilisée.

~~~~text
### Requirement: Identité et FQDN explicites

Chaque Domaine MUST posséder une identité stable et un FQDN DNS explicitement choisi. Deux Domaines d'une même Instance MUST NOT déclarer le même FQDN exact. La position DNS MUST NOT créer d'approbation ni d'autorisation implicite.

#### Scenario: Racine déjà utilisée

- **WHEN** un Domaine demande le FQDN exact d’un autre Domaine de l’Instance
- **THEN** la déclaration est refusée avant activation.
~~~~

### Référence courante pixs-domains-686f4e13ff70

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 20. SHA-256 : `686f4e13ff70e8af073de2ac6f80d25d553a84feb6cec9fec11dc0f13c5d93cc`.

Scénarios : Deux sous-domaines; Faux suffixe.

~~~~text
### Requirement: ZT obligatoire dédié ou partagé

Chaque Domaine MUST utiliser une instance ZT. Il MAY créer son ZT ou utiliser celui de l'Instance lorsque son FQDN est égal au FQDN ZT ou en est un sous-domaine par labels DNS. Plusieurs Domaines admissibles MAY utiliser ce même ZT ; le partage MUST rester explicitement déclaré.

#### Scenario: Deux sous-domaines

- **WHEN** association.pixs.fr et recherche.pixs.fr choisissent le ZT pixs.fr
- **THEN** ils peuvent être rattachés avec des périmètres distincts.

#### Scenario: Faux suffixe

- **WHEN** association-autrepixs.fr demande le ZT pixs.fr en invoquant un suffixe de caractères
- **THEN** la condition hiérarchique DNS est refusée.
~~~~

### Référence courante pixs-domains-bd2991264b73

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 34. SHA-256 : `bd2991264b73d60314f90b7bb3d936bee405c507992fe50e7ff2e06fb1da6fc6`.

Scénarios : Même ZT sans politique.

~~~~text
### Requirement: Isolation dans un ZT partagé

Les politiques MUST pouvoir être propres à un Domaine ou partagées explicitement. Les communications inter-domaines MUST être refusées par défaut et nécessiter une politique explicite. Le partage du ZT MUST NOT fusionner les identités, ACL applicatives, annuaires ou realms.

#### Scenario: Même ZT sans politique

- **WHEN** deux acteurs de Domaines différents partagent ZT sans autorisation de communication
- **THEN** l’initiation inter-domaines est refusée.
~~~~

### Référence courante pixs-domains-c9ce061e2b23

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 43. SHA-256 : `c9ce061e2b23d3859a4cb92e01635334908d63f103ce5c9db7b2b2c1d5a053c5`.

Scénarios : ZT partagé et KZT manquant.

~~~~text
### Requirement: Services minimaux par Domaine

Chaque Domaine MUST disposer de sa PG indépendante, de ses organigrammes organisationnel/fonctionnel, d'au moins un LZT/OpenLDAP et d'un KZT/MIT Kerberos. Chaque Domaine MUST déclarer son realm, unique dans l'Instance. Les minima CZT/SZT/RZT/STZT/DZT/PKIZT MUST être évalués par ZT réel, pas dupliqués par déduction pour un ZT partagé.

#### Scenario: ZT partagé et KZT manquant

- **WHEN** un nouveau Domaine partage un ZT opérationnel mais ne possède aucun KZT
- **THEN** ses services de Domaine restent non opérationnels tant que ce minimum manque.
~~~~

### Référence courante pixs-domains-784b3416b755

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 52. SHA-256 : `784b3416b7559266c7a1b38d15a475ebd8b05a90e2f00eb976a8bf198703e0f4`.

Scénarios : Domaine sans tenant; Tenant rattaché deux fois.

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

### Référence courante pixs-domains-8e5157150f7c

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 66. SHA-256 : `8e5157150f7c0a1801085b1c19bdd9c69fe4c345dcba246bb25ed2aba4727793`.

Scénarios : Affiliation sans admission.

~~~~text
### Requirement: Individus et identités multiples

Un individu Core MUST pouvoir être affilié à plusieurs Domaines et tenants et posséder plusieurs identités par Domaine. Chaque participation MUST conserver ses admissions, profils et habilitations. Une affiliation Core MUST NOT valoir admission ZT, sauf politique automatique explicite.

#### Scenario: Affiliation sans admission

- **WHEN** un individu est affilié à Recherche sans politique d’admission automatique
- **THEN** son appartenance ZT n’est pas créée par cette seule affiliation.
~~~~

### Référence courante pixs-domains-ba4dfa97bf7d

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 75. SHA-256 : `ba4dfa97bf7dfe8389d5a8f4597671aa9630b9e24d13f8a2ea071bc82dc36b12`.

Scénarios : Tenant transféré.

~~~~text
### Requirement: Transferts fonctionnels contrôlés V1

La V1 MUST prévoir les transferts autorisés d'identités numériques, données métier et tenants entre Domaines de la même Instance, avec vérification des dépendances, continuité des références et réévaluation des droits cibles. Le transfert MUST NOT copier implicitement des autorisations ni être présenté comme déplacement d'une brique exécutable.

#### Scenario: Tenant transféré

- **WHEN** un transfert de tenant est engagé entre deux Domaines
- **THEN** son identité est conservée, son propriétaire est unique et les habilitations de destination sont réévaluées.
~~~~

### Référence courante pixs-domains-2d4b91559aa3

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 84. SHA-256 : `2d4b91559aa387da2cb8be333d66674748a755850567e45bba8b742811112985`.

Scénarios : Transfert de département.

~~~~text
### Requirement: Structures organisationnelles non transférables V1

La V1 MUST NOT proposer le transfert fonctionnel de structures organisationnelles entre Domaines. Miroitage autorisé et réorganisation interne MUST rester distincts d'un tel transfert.

#### Scenario: Transfert de département

- **WHEN** une demande V1 vise à transférer un département entre Domaines
- **THEN** elle est refusée comme hors périmètre sans modifier les structures source ou cible.
~~~~

### Référence courante pixs-domains-f9d0dad1d882

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 93. SHA-256 : `f9d0dad1d882e815cf4d5b665b2037e6591dcb271ed3dd1e9f7605fcd4759334`.

Scénarios : Dernier Domaine.

~~~~text
### Requirement: Retrait du premier Domaine

Le premier Domaine MAY être retiré par procédure explicite si au moins un autre Domaine est opérationnel et si données, identités, authentification globale et dépendances sont traitées. Le retrait MUST NOT rétablir Standalone, laisser l'administration sans identité admissible ou retirer un ZT partagé encore requis.

#### Scenario: Dernier Domaine

- **WHEN** le retrait vise le seul Domaine opérationnel
- **THEN** il est refusé sans retour implicite en Standalone.
~~~~

### Référence courante pixs-domains-94814997f512

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 102. SHA-256 : `94814997f512912fbd83b186f7db3bf2f0771d0e37c0e5ecfc7fe81a41c5562f`.

Scénarios : Individu externe reconnu.

~~~~text
### Requirement: Approbations internes et externes

Les Domaines MUST pouvoir établir des approbations dans une même Instance ou entre Instances selon zt-instances. Un individu externe MUST conserver son identité d'origine ; la cible MUST conserver une référence et décider séparément de ses admissions et droits. Les composantes DNS et Kerberos MUST être explicites.

#### Scenario: Individu externe reconnu

- **WHEN** une approbation permet de reconnaître l’identité externe
- **THEN** la reconnaissance ne crée pas d’identité locale indépendante ou de droits automatiques.
~~~~

### Référence courante pixs-domains-d8fce09ab784

Source : [pixs-domains](../../specs/pixs-domains/spec.md), ligne 111. SHA-256 : `d8fce09ab78488325720197abff25a3f229a41ca7f6e38dac7da16c02df7b924`.

Scénarios : Reconstruction de Domaine.

~~~~text
### Requirement: Références PG et services de Domaine en mode normal ou critique

LZT et KZT MUST être obligatoires par Domaine. PG MUST rester souveraine pour les données de référence Pixs ; LDAP MUST porter l'état opérationnel Kerberos durable en mode normal. Une reconstruction complète depuis PG MUST suivre le mode critique autorisé, avec restauration protégée ou recréation/reprovisionnement selon profil et sauvegardes disponibles. La réplication LDAP MUST NOT remplacer la référence Core PG.

#### Scenario: Reconstruction de Domaine

- **WHEN** tous les annuaires du Domaine sont perdus
- **THEN** le Domaine applique sa procédure critique, distingue données de référence et clés récupérées/recréées, puis vérifie la remise en service.
~~~~

### Référence courante zt-instances-8b936c8ce6e3

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 11. SHA-256 : `8b936c8ce6e344379ce474d3e036ea3c138a8c25a154f7e995d4f69968aee74b`.

Scénarios : Plusieurs composants sur un hôte.

~~~~text
### Requirement: Acteurs et identité persistante

ZT MUST distinguer acteurs humains, matériels, logiciels et organisationnels. Un acteur technique MUST avoir identité, responsabilités et cycle de vie distincts de ses rôles, processus et hôte. Hôte, PBO, PA et PZT MUST conserver leurs identités propres ; les rôles MAY être cumulés explicitement sous les incompatibilités applicables.

#### Scenario: Plusieurs composants sur un hôte

- **WHEN** PBO, PA et PZT sont cohébergés
- **THEN** leur cohébergement ne fusionne ni identités ni habilitations.
~~~~

### Référence courante zt-instances-02f45c3fc9a4

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 20. SHA-256 : `02f45c3fc9a4f05a2ee8f47761142ae718a760009568649070e52b7e3c6dc4c4`.

Scénarios : Individu dans deux ZT.

~~~~text
### Requirement: Appartenances selon la catégorie

Un acteur non humain MUST appartenir à une seule instance ZT à la fois. Un individu Core MAY être admis dans plusieurs ZT ; chaque admission MUST conserver affiliations et permissions indépendantes. Une relation d'approbation MUST NOT changer l'appartenance du représentant ou du partenaire.

#### Scenario: Individu dans deux ZT

- **WHEN** un individu est admis dans deux ZT
- **THEN** chaque ZT décide séparément de ses droits sans copie automatique.
~~~~

### Référence courante zt-instances-6518a8a762d8

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 29. SHA-256 : `6518a8a762d878c26443bdc3b6ad94fcb18c14dadc87ac3f5ceb1c9c25f68790`.

Scénarios : Délégation limitée.

~~~~text
### Requirement: Gouvernance commune et délégations

Chaque ZT MUST avoir une gouvernance commune, éventuellement collective, avec compétences explicites. Admission et gestion des approbations MAY être déléguées par périmètre ; chaque délégataire MUST rester dans son mandat sans élargir l'autorité de l'Instance ou des Domaines.

#### Scenario: Délégation limitée

- **WHEN** un délégué aux approbations d’un périmètre vise un autre périmètre
- **THEN** la création ou modification hors mandat est refusée.
~~~~

### Référence courante zt-instances-fe908c4cf04e

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 38. SHA-256 : `fe908c4cf04e403c81b93c34449ff1ce0bb362d1d81a14a5aa6bd53867698626`.

Scénarios : Rejeu d’enrôlement.

~~~~text
### Requirement: Admission administrative et préautorisation

L'admission administrative MUST être le défaut pour les individus. Une admission automatique MUST exiger une politique explicite. L'enrôlement préautorisé MUST utiliser un jeton individuel temporaire à usage unique, avec engagement et reprise évitant double identité ou réutilisation.

#### Scenario: Rejeu d’enrôlement

- **WHEN** un jeton déjà consommé est présenté pour un nouveau membre
- **THEN** il ne crée pas de seconde admission.
~~~~

### Référence courante zt-instances-b0acd891069f

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 47. SHA-256 : `b0acd891069f982f41c1860ebc7a698a5c3fec2141afbaea754cce16f6c6d4bd`.

Scénarios : Admission expirée après restauration.

~~~~text
### Requirement: Participations permanentes et temporaires

L'appartenance permanente MUST être proposée par défaut ; les profils temporaires/éphémères MUST avoir échéance finie et renouvellement autorisé. Les autorisations MUST NOT dépasser la participation. Redémarrage ou restauration MUST NOT repousser l'échéance ; la fin d'appartenance MUST NOT supprimer implicitement l'individu ou l'environnement.

#### Scenario: Admission expirée après restauration

- **WHEN** une sauvegarde contient une admission désormais expirée
- **THEN** aucun accès n’est réarmé et les données/hôtes ne sont pas supprimés par déduction.
~~~~

### Référence courante zt-instances-abd1a7f7a384

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 56. SHA-256 : `abd1a7f7a3844fc63953eda5d7ff8c95f8f0b01b94f94ab592c0eeb2ce7414c7`.

Scénarios : Chaîne trop profonde.

~~~~text
### Requirement: Approbations directionnelles et bornées

Une approbation MUST déclarer source, destinataire, portée, conditions et délégations autorisées. La réciprocité MUST exiger deux approbations. La transitivité MUST être autorisée explicitement avec profondeur maximale finie configurable ; chaque maillon MUST respecter les limites des relations traversées. Reconnaître une identité MUST NOT accorder des droits sur les ressources.

#### Scenario: Chaîne trop profonde

- **WHEN** une chaîne dépasse la profondeur admise par un maillon
- **THEN** la reconnaissance indirecte est refusée même si les autres maillons l’acceptent.
~~~~

### Référence courante zt-instances-b9367d6d6b27

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 65. SHA-256 : `b9367d6d6b279030ffb9cb85e35b97d72f23d1b94a5b5665c53bb22ca15dcd19`.

Scénarios : Sens inverse.

~~~~text
### Requirement: Politiques durables et autorisations bornées

Les politiques ZT MUST être durables ; les autorisations d'exécution MUST être temporaires et bornées. Permissions individuelles/collectives MUST viser services, directions, protocoles et ports déclarés avec interdiction prioritaire et refus par défaut selon les contrats applicables. L'initiation inverse MUST nécessiter sa propre autorisation et les réponses MUST rester encadrées.

#### Scenario: Sens inverse

- **WHEN** une destination autorisée à répondre initie une nouvelle communication inverse
- **THEN** cette initiation est refusée sans permission distincte.
~~~~

### Référence courante zt-instances-cc529473dd70

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 74. SHA-256 : `cc529473dd70e8a2099d093781f28835b1adfc0e367f27415468e48745448114`.

Scénarios : Logiciel sans droit.

~~~~text
### Requirement: Appartenance et preuve sans permission implicite

Un certificat, une IP, un rôle administratif, une affiliation ou un positionnement hiérarchique MUST NOT suffire à accorder l'accès. Les permissions d'utilisation et d'administration MUST être distinguées. Lorsqu'un contexte humain est requis, les droits de l'individu et ceux de l'acteur technique MUST être vérifiés conjointement.

#### Scenario: Logiciel sans droit

- **WHEN** un individu habilité agit par un logiciel non habilité sur la cible
- **THEN** l’action nécessitant les deux permissions est refusée.
~~~~

### Référence courante zt-instances-4208f537345f

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 83. SHA-256 : `4208f537345fc9a96a01cd5319734cc7a9788e7e3ca565903ba89532d908db50`.

Scénarios : Relais non mandaté.

~~~~text
### Requirement: Représentation explicite et indépendante

La participation MAY être directe ou représentée. Le mandat MUST identifier représenté, représentant, actions, ressources, durée, révocation et éventuelle redélégation. Le représenté MUST conserver son identité ; le représentant MUST utiliser ses moyens propres sans recevoir les secrets personnels de l'individu et sans transférer un pouvoir absent du représenté.

#### Scenario: Relais non mandaté

- **WHEN** un logiciel relaie une requête sans mandat de représentation
- **THEN** ce relais n’établit pas le droit d’agir au nom de l’individu.
~~~~

### Référence courante zt-instances-906ddd8e7c4a

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 92. SHA-256 : `906ddd8e7c4a0c8c888a6fd2b2b733e2490664201a2f103475502d14f07797a0`.

Scénarios : Tâche longue.

~~~~text
### Requirement: Mandats et session

Le mandat humain MUST dépendre de la session par défaut. Une indépendance de session MAY être autorisée explicitement avec ses propres bornes. Suspension de l'individu, retrait des droits ou révocation MUST conserver leurs effets sur le mandat indépendant.

#### Scenario: Tâche longue

- **WHEN** un mandat indépendant autorisé continue après une déconnexion ordinaire
- **THEN** il reste limité à sa durée et cesse si ses droits ou son mandat sont révoqués.
~~~~

### Référence courante zt-instances-9e1b32b3ada0

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 101. SHA-256 : `9e1b32b3ada0a358695a5cc175a08e55c41d59556cb16a12ba7c2b867b28ea03`.

Scénarios : Auth indisponible.

~~~~text
### Requirement: Propagation des états autoritatifs

Une suspension Core MUST suspendre l'exercice des droits dépendants et réévaluer les mandats. La révocation de session MUST invalider les autorisations qui en dépendent. Une panne Core/Auth MUST suivre la continuité bornée sans valoir révocation ou nouvelle permission. La remise en activité MUST réévaluer l'état courant sans restauration implicite.

#### Scenario: Auth indisponible

- **WHEN** Auth devient temporairement injoignable
- **THEN** seules les opérations encore admissibles dans leur continuité bornée restent possibles.
~~~~

### Référence courante zt-instances-e45def8cb779

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 110. SHA-256 : `e45def8cb77933a3585cbf97fcda38c225e26cd984dffdd430237d9eef23ca30`.

Scénarios : Minima partagés.

~~~~text
### Requirement: Socle et minima opérationnels ZT

Chaque ZT MUST disposer d'au moins un PZT portant initialement CZT, SZT, RZT, STZT, DZT et PKIZT. Les rôles MAY être répartis et redondés. Le premier PZT complet V1 MUST cibler Debian/Linux ; les suivants MUST porter seulement les rôles qualifiés pour leur plateforme. GZT, EZT et RPZT MUST être optionnels et désactivés par défaut.

#### Scenario: Minima partagés

- **WHEN** deux Domaines utilisent le même ZT
- **THEN** les minima sont évalués sur ce ZT réel et les périmètres restent séparés.
~~~~

### Référence courante zt-instances-b6e16e2c94a8

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 119. SHA-256 : `b6e16e2c94a830d2873dca9721345de994a8de38ac26a6907f369aecc1958398`.

Scénarios : Rôle déclaré sans exécutant.

~~~~text
### Requirement: Existence et disponibilité distinctes

La gestion MUST distinguer rôle déclaré, admis, configuré et opérationnel vérifié. Une panne MUST dégrader seulement les capacités concernées lorsque leur isolation est démontrée. Une mesure ancienne ou un processus vivant MUST NOT prouver le service actuel.

#### Scenario: Rôle déclaré sans exécutant

- **WHEN** DZT est déclaré mais aucun service admissible ne répond
- **THEN** la gestion expose l’indisponibilité au lieu d’un DNS actif fictif.
~~~~

### Référence courante zt-instances-a979db4ef59b

Source : [zt-instances](../../specs/zt-instances/spec.md), ligne 128. SHA-256 : `a979db4ef59bb6aadfac590f7db6187897b89e571759f190851cf3022afe88c9`.

Scénarios : Révocation d’un PZT.

~~~~text
### Requirement: Sortie et révocation séparées

La sortie planifiée, la révocation et le changement de mode MUST avoir des procédures distinctes et explicites. Le retrait MUST préserver les historiques et traiter les dépendances sans créer un changement de mode implicite ni détruire les ressources hors mandat.

#### Scenario: Révocation d’un PZT

- **WHEN** un PZT est révoqué
- **THEN** ses accès sont retirés selon le contrat sans bascule automatique de l’Instance en Standalone.
~~~~
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->
