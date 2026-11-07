# Exigences de réalisation — C13

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Références courantes du périmètre validé

Les copies plus anciennes conservées dans ce fichier sont historiques. Seuls les blocs ci-dessous correspondent au référentiel de la cible consolidée. Ils ne sont pas des deltas à synchroniser et ne prouvent aucune implémentation.

| Capacité | Exigence | Scénarios | Référence |
|---|---|---:|---|
| pixs-instance | Identité logique et référentiel commun | 1 | pixs-instance-b9b134df059f |
| pixs-instance | Modes Standalone ZT et Domaine | 2 | pixs-instance-18485b8d2051 |
| pixs-instance | ZT entièrement initialisé avant Domaine | 2 | pixs-instance-81a8ae9c0556 |
| pixs-instance | Minima et contrôleurs distincts | 1 | pixs-instance-b189f9cd6424 |
| pixs-instance | Références PG avant et après Domaine | 1 | pixs-instance-9baefb0c5ae7 |
| pixs-instance | Maintenance des écritures pour la transition | 1 | pixs-instance-ebdd233f14af |
| pixs-instance | Administration globale par identités habilitées | 1 | pixs-instance-8c964dc84f92 |
| pixs-instance | Absence de retour Domaine Standalone V1 | 1 | pixs-instance-c159a59d2125 |
| pixs-instance | Habilitations Instance et domaines | 1 | pixs-instance-b7a2b5d23968 |
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
| organization-charts | Trois référentiels propriétaires | 1 | organization-charts-c0cec12f0548 |
| organization-charts | Hiérarchie structurelle et affiliations | 1 | organization-charts-43a3193484d2 |
| organization-charts | Source explicite de chaque miroir | 1 | organization-charts-8369220fda62 |
| organization-charts | Structure seule par défaut | 1 | organization-charts-3f5fd5146131 |
| organization-charts | Admission et droits séparés du miroir | 1 | organization-charts-a06107e07b95 |

### Référence courante pixs-instance-b9b134df059f

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 11. SHA-256 : `b9b134df059f8bf6661d4623bae95e040e6f1461c35dd19d5d91ec4cd68c99bc`.

Scénarios : Ajout de PBO.

~~~~text
### Requirement: Identité logique et référentiel commun

L'Instance Pixs MUST posséder une identité stable distincte de ses PBO, processus, hôtes et ZT. Tous ses PBO MUST utiliser le même référentiel d'individus Core ; un nouveau PBO MUST NOT créer une liste concurrente d'individus.

#### Scenario: Ajout de PBO

- **WHEN** un second PBO est admis dans la même Instance
- **THEN** il référence les individus communs tout en conservant les données et responsabilités de ses modules.
~~~~

### Référence courante pixs-instance-18485b8d2051

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 20. SHA-256 : `18485b8d20510d544246b6d9c7efd51c9479aedb4fd4f839499c3e12bed5f82b`.

Scénarios : Transport pré-domaine; Mode ZT.

~~~~text
### Requirement: Modes Standalone ZT et Domaine

L'Instance MUST distinguer Standalone sans Domaine et avec une application PBO logique éventuellement redondée, ZT sans Domaine avec un ZT d'Instance, et Domaine avec un ou plusieurs Domaines utilisant ZT. Plusieurs PBO fonctionnellement distincts MAY exister en ZT et Domaine. Ces modes MUST rester distincts de Nuitka standalone et de l'activation du transport PZT.

#### Scenario: Transport pré-domaine

- **WHEN** Standalone utilise PZT pour joindre PA
- **THEN** le mode reste Standalone et les contrôles réseau et applicatifs restent nécessaires.

#### Scenario: Mode ZT

- **WHEN** ZT est initialisé sans création de Domaine
- **THEN** le référentiel des individus et les données pré-domaine restent au niveau Instance.
~~~~

### Référence courante pixs-instance-81a8ae9c0556

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 34. SHA-256 : `81a8ae9c0556560bcabef991ba7a8b2259c107021aadecec007049cbc2a8898f`.

Scénarios : ZT incomplet; Préconditions vérifiées.

~~~~text
### Requirement: ZT entièrement initialisé avant Domaine

La création du premier Domaine MUST exiger un mode ZT complètement initialisé, avec rôles essentiels opérationnels, identités, stockage et politiques vérifiés. Un état administratif créé ou un processus vivant MUST NOT suffire. La transition MUST être explicite et suivie durablement.

#### Scenario: ZT incomplet

- **WHEN** le rôle PKIZT essentiel manque lors de la demande du premier Domaine
- **THEN** la transition reste bloquée avec les capacités manquantes identifiées.

#### Scenario: Préconditions vérifiées

- **WHEN** le ZT et les autres préconditions de transition sont vérifiés
- **THEN** la procédure autorisée peut préparer puis activer le premier Domaine.
~~~~

### Référence courante pixs-instance-b189f9cd6424

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 48. SHA-256 : `b189f9cd6424f6b3127b840e6d069becb563c5a7942465fed2bd469482045888`.

Scénarios : Contrôleurs regroupés.

~~~~text
### Requirement: Minima et contrôleurs distincts

Chaque Instance MUST disposer d'au moins un PBO et un PA, déployés selon les environnements à administrer. Les contrôleurs d'Instance et de Domaine MUST être distingués du CZT. Leur regroupement ou séparation sur des PBO MUST être configurable sans fusion de bases ni habilitations.

#### Scenario: Contrôleurs regroupés

- **WHEN** un PBO assure les fonctions Instance et Domaine
- **THEN** les propriétaires des bases, identités et autorisations restent distincts.
~~~~

### Référence courante pixs-instance-9baefb0c5ae7

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 57. SHA-256 : `9baefb0c5ae783cb168944c78c34b6f7bc7814b244f9c8888e21389eef0e6e37`.

Scénarios : Activation du premier Domaine.

~~~~text
### Requirement: Références PG avant et après Domaine

Avant le premier Domaine, PG Instance MUST porter individus, identités numériques, organigrammes Core, groupes, ACL et données métier pré-domaine. Après activation, PG Instance MUST conserver les individus et données communes sans identité numérique d'Instance ; les identités et données reprises MUST appartenir à PG du premier Domaine, avec identifiants et relations préservés.

#### Scenario: Activation du premier Domaine

- **WHEN** le transfert pré-domaine est confirmé
- **THEN** l’identité de Domaine devient utilisable selon son profil et l’ancienne identité d’Instance ne reste pas une autre voie de connexion.
~~~~

### Référence courante pixs-instance-ebdd233f14af

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 66. SHA-256 : `ebdd233f14afcc75b3a6a94757dd20a6eb5ec1c9e93b692f109025695c0b8e33`.

Scénarios : Interruption de transfert.

~~~~text
### Requirement: Maintenance des écritures pour la transition

La transition pré-domaine vers Domaine MUST planifier une maintenance des écritures, vérifier données, relations et authentification cible et traiter toute issue inconnue avant reprise. Elle MUST NOT déclarer la bascule réussie sur un accusé de réception ou un seul effet technique PA.

#### Scenario: Interruption de transfert

- **WHEN** le résultat du transfert ou de son engagement est inconnu
- **THEN** la procédure réconcilie les états propriétaires avant toute répétition ou reprise des écritures.
~~~~

### Référence courante pixs-instance-8c964dc84f92

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 75. SHA-256 : `8c964dc84f92c940b5c3ba094d124ffaeb003db84c0f5617cc9487e8d70c38e3`.

Scénarios : Domaine d’authentification non habilité.

~~~~text
### Requirement: Administration globale par identités habilitées

Après activation du premier Domaine, l'administration globale MUST utiliser des identités de Domaines explicitement habilitées. Plusieurs Domaines d'authentification MAY être autorisés. Une panne LDAP/Kerberos MAY être traitée par un profil PG Domaine explicitement autorisé et qualifié ; elle MUST NOT recréer d'identité numérique d'Instance ni réduire l'assurance exigée.

#### Scenario: Domaine d’authentification non habilité

- **WHEN** un utilisateur authentifié par un Domaine non habilité demande l’administration globale
- **THEN** la demande est refusée malgré la validité de son authentification.
~~~~

### Référence courante pixs-instance-c159a59d2125

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 84. SHA-256 : `c159a59d212509364156279d995f289887b68dc5fde0e1bc12244c0f317d5cfa`.

Scénarios : Ancienne sauvegarde.

~~~~text
### Requirement: Absence de retour Domaine Standalone V1

Après activation du premier Domaine, l'Instance MUST rester en mode Domaine en V1. Panne, restauration, retrait de domaine ou révocation MUST NOT provoquer un retour Standalone ou réactiver les anciennes identités. Les autres transitions inverses non spécifiées MUST NOT être introduites implicitement.

#### Scenario: Ancienne sauvegarde

- **WHEN** une reprise utilise des données antérieures à la transition
- **THEN** les contrôles empêchent de rétablir le mode et les identités Standalone devenus caducs.
~~~~

### Référence courante pixs-instance-b7a2b5d23968

Source : [pixs-instance](../../specs/pixs-instance/spec.md), ligne 93. SHA-256 : `b7a2b5d2396839fee82af4ccc545e2c2c542dcbef6458888992a032fce8e929f`.

Scénarios : PBO mutualisé.

~~~~text
### Requirement: Habilitations Instance et domaines

Les habilitations globales Instance et celles de chaque Domaine MUST être séparées et vérifiées. Le partage d'un PBO, PA, stockage physique ou réseau MUST NOT les transmettre implicitement.

#### Scenario: PBO mutualisé

- **WHEN** un administrateur d’un Domaine utilise un PBO servant plusieurs Domaines
- **THEN** son action reste limitée aux périmètres explicitement autorisés.
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

### Référence courante organization-charts-c0cec12f0548

Source : [organization-charts](../../specs/organization-charts/spec.md), ligne 11. SHA-256 : `c0cec12f054833f37f9ef4e5d2ae8e89737e329ea5b1f9ce56459b44fffdf241`.

Scénarios : ZT partagé.

~~~~text
### Requirement: Trois référentiels propriétaires

Core MUST gérer l'organigramme organisationnel et le fonctionnel, par Domaine après transition. CZT MUST gérer l'organigramme structurel de son ZT. PBO MUST présenter trois volets distincts ; un ZT partagé MUST conserver les périmètres des Domaines sans dupliquer une racine ZT par Domaine.

#### Scenario: ZT partagé

- **WHEN** deux Domaines utilisent le même CZT
- **THEN** leurs volets Core restent propres et les périmètres structurels sont présentés dans le ZT commun.
~~~~

### Référence courante organization-charts-43a3193484d2

Source : [organization-charts](../../specs/organization-charts/spec.md), ligne 20. SHA-256 : `43a3193484d2bee52ef6f44cfe182b5c6b34e2cfb44d4f63bcd89d3ed21ebcd1`.

Scénarios : Deux parents structurels.

~~~~text
### Requirement: Hiérarchie structurelle et affiliations

L'organigramme ZT MUST posséder une racine unique, au plus un parent structurel par structure, aucun cycle et des affiliations multiples possibles. Chaque acteur technique MUST avoir une structure responsable de référence ; chaque individu MUST avoir un rattachement principal par ZT. Ces relations MUST rester distinctes des permissions et de la hiérarchie PKI.

#### Scenario: Deux parents structurels

- **WHEN** une structure ZT reçoit deux parents structurels
- **THEN** la mutation est refusée sans empêcher les affiliations transversales autorisées.
~~~~

### Référence courante organization-charts-8369220fda62

Source : [organization-charts](../../specs/organization-charts/spec.md), ligne 29. SHA-256 : `8369220fda6234df9ed1556288de294305748cfda265cac54698c3df3fa38184`.

Scénarios : Écriture sur miroir.

~~~~text
### Requirement: Source explicite de chaque miroir

Un périmètre de miroitage MUST choisir une source explicite parmi les trois organigrammes, ses données et transformations autorisées. Ses mutations MUST passer par la source et respecter les contraintes cibles. Une modification de la copie MUST NOT devenir silencieusement une deuxième autorité.

#### Scenario: Écriture sur miroir

- **WHEN** un opérateur tente de modifier directement la copie reflétée
- **THEN** l’interface applique le contrat de la source ou refuse l’écriture concurrente.
~~~~

### Référence courante organization-charts-3f5fd5146131

Source : [organization-charts](../../specs/organization-charts/spec.md), ligne 38. SHA-256 : `3f5fd5146131f61a9cf1d8e9811329be5f7f571d315ad76e8af0231f736a8105`.

Scénarios : Miroir standard.

~~~~text
### Requirement: Structure seule par défaut

Le miroir MUST porter sur la structure seule par défaut. La synchronisation des rattachements et affiliations MAY être activée explicitement par périmètre ; les individus MUST rester référencés depuis Core sans duplication d'identité ou de moyen d'authentification.

#### Scenario: Miroir standard

- **WHEN** un miroir est créé sans sélection des affiliations
- **THEN** les seules structures et relations hiérarchiques autorisées sont reprises.
~~~~

### Référence courante organization-charts-a06107e07b95

Source : [organization-charts](../../specs/organization-charts/spec.md), ligne 47. SHA-256 : `a06107e07b9597bbf983057cb15e8480fd7a774f5e4c3628bc1d29e71ecce71b`.

Scénarios : Affiliation vers un ZT.

~~~~text
### Requirement: Admission et droits séparés du miroir

Un miroir MUST NOT créer implicitement admission ZT, compte, permission ou copie d'ACL. Une affiliation vers ZT MUST exiger l'admission applicable et les politiques ZT MUST être réévaluées après modification autorisée.

#### Scenario: Affiliation vers un ZT

- **WHEN** le miroir reçoit l’affiliation d’un individu non admis
- **THEN** aucune participation effective ni autorisation ZT n’est déduite.
~~~~
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

Cette table est une référence au canon, sans delta et sans altération de ses exigences. Les textes complets et tous leurs scénarios restent applicables selon leurs conditions. Le profil C00 adopté le 18 octobre 2026 et intégré au canon apporte les précisions de première livraison ; il ne supprime aucun MUST existant.

Les lignes et empreintes désignent l’instant de préparation ; une dérive impose une nouvelle lecture avant réalisation. La sélection ci-dessous part de la matrice et doit être affinée par clause, sans annoncer que tous les scénarios ont déjà été vérifiés.

| Capacité / ligne | Exigence | Statut de matrice | Scénarios sources |
|---|---|---|---|
| accessibility / 8 | [Niveau cible WCAG 2.2 AA](../../specs/accessibility/spec.md#L8) | P | Contribution non conforme |
| accessibility / 17 | [Fonctionnement clavier et technologies d'assistance](../../specs/accessibility/spec.md#L17) | P | Parcours clavier complet |
| accessibility / 26 | [Sémantique native préservée](../../specs/accessibility/spec.md#L26) | P | Rôle ARIA redondant |
| accessibility / 35 | [Validation outillée et manuelle combinées](../../specs/accessibility/spec.md#L35) | P | Défaut non détectable automatiquement |
| audit / 8 | [Audit dérogeable du Super Admin](../../specs/audit/spec.md#L8) | P | Opération Super Admin sans audit persistant ; Audit ordinaire toujours obligatoire |
| audit / 23 | [Portée de l'exception dans les exigences d'audit](../../specs/audit/spec.md#L23) | P | Profil d'occultation inchangé |
| audit / 32 | [Audit fonctionnel distinct des logs techniques](../../specs/audit/spec.md#L32) | P | Perte de télémétrie technique |
| audit / 41 | [Contenu minimal d'un événement d'audit](../../specs/audit/spec.md#L41) | P | Refus d'autorisation tracé |
| audit / 50 | [Périmètre obligatoire d'audit](../../specs/audit/spec.md#L50) | P | Opération destructive sans audit |
| audit / 59 | [Append-only et réécriture contrôlée](../../specs/audit/spec.md#L59) | P | Obligation d'effacement |
| audit / 68 | [Minimisation et non-duplication des données](../../specs/audit/spec.md#L68) | P | Payload sensible détecté |
| audit / 77 | [Audit exhaustif du panneau d'administration](../../specs/audit/spec.md#L77) | P | Navigation non auditable |
| authorization / 8 | [Portée du contrôle total du Super Admin](../../specs/authorization/spec.md#L8) | P | Tenant non accordé au Super Admin ; Tenant accordé malgré un refus ACL |
| authorization / 23 | [Exception Super Admin dans toutes les interfaces](../../specs/authorization/spec.md#L23) | P | Même exception selon la façade |
| authorization / 33 | [Contrôles applicatifs dérogeables par le Super Admin](../../specs/authorization/spec.md#L33) | P | Contrôle applicatif dérogé |
| authorization / 43 | [Priorité transversale de l'exception Super Admin](../../specs/authorization/spec.md#L43) | P | Compte ordinaire sans exception ; Contrat structurel sans privilège |
| authorization / 57 | [Modèle Subject Resource Action Context](../../specs/authorization/spec.md#L57) | P | Propriété sans politique refusée |
| authorization / 66 | [Priorité DENY puis ALLOW puis refus](../../specs/authorization/spec.md#L66) | P | Conflit DENY contre ALLOW |
| authorization / 77 | [Évaluation applicative avant exposition](../../specs/authorization/spec.md#L77) | P | Liste filtrée à la source |
| authorization-engine / 8 | [Exception Super Admin distincte des profils préparatoires](../../specs/authorization-engine/spec.md#L8) | P | Profils préparatoires sans privilège ajouté |
| authorization-engine / 17 | [Politiques déclaratives versionnées](../../specs/authorization-engine/spec.md#L17) | P | Politique à code rejetée |
| authorization-engine / 26 | [Décisions et filtrage tracés](../../specs/authorization-engine/spec.md#L26) | P | Décision périmée non réutilisée |
| authorization-engine / 37 | [Groupes bornés et délégation auditée](../../specs/authorization-engine/spec.md#L37) | P | Moteur indisponible |
| authorization-engine / 48 | [Profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L48) | P | Sélecteur générique refusé |
| authorization-engine / 57 | [Conditions typées du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L57) | P | Booléen distinct d'un entier |
| authorization-engine / 68 | [Assurances et faits du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L68) | P | Fait inconnu refusé fermé ; Assurances non substituables |
| authorization-engine / 82 | [Limites et obligations du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L82) | P | Obligation inconnue rejetée |
| authorization-engine / 91 | [Obligations honorées par le PEP du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L91) | P | ALLOW minimal avec obligation honorée |
| authorization-engine / 100 | [Snapshot et priorité du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L100) | P | DENY prévaut sur ALLOW mêmes cibles |
| authorization-engine / 109 | [Calcul d'expiration du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L109) | P | Auth expirée malgré TTL |
| authorization-engine / 120 | [Transitions temporelles et réévaluation du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L120) | P | ALLOW expire à activation future DENY |
| authorization-engine / 129 | [Confiance backend et diagnostics du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L129) | P | Booléen client insuffisant |
| authorization-engine / 140 | [Plateforme et intertenant du profil PDP minimal fermé v1](../../specs/authorization-engine/spec.md#L140) | P | Intertenant minimal refusé ; Plateforme ALLOW explicite ; Plateforme sans explicite refusée |
| design-system / 8 | [Tokens sémantiques d'intention](../../specs/design-system/spec.md#L8) | P | Valeur brute refusée |
| design-system / 17 | [Primitives à API stable](../../specs/design-system/spec.md#L17) | P | Variante non déclarée |
| design-system / 26 | [Cohérence Light et Dark par les tokens](../../specs/design-system/spec.md#L26) | P | Primitive inspectée dans les deux modes |
| design-system / 35 | [Adapter de rendu sans contournement](../../specs/design-system/spec.md#L35) | P | Accès direct au moteur refusé |
| frontend / 8 | [Contributions déclarées et routage sans collision](../../specs/frontend/spec.md#L8) | P | Route ambiguë bloquée |
| frontend / 17 | [Session fournie par le shell et autorisation applicative](../../specs/frontend/spec.md#L17) | P | Garde frontale non substitutive |
| frontend / 26 | [Mutations provisoires et invalidation tenant-aware](../../specs/frontend/spec.md#L26) | P | Invalidation après commande |
| frontend / 37 | [Sous-modularité frontend par le modèle de composants commun](../../specs/frontend/spec.md#L37) | P | Sous-module optionnel isolé |
| initial-administration / 11 | [Compte Super Admin unique de paramétrage et de secours](../../specs/initial-administration/spec.md#L11) | ND | Compte fonctionnel non nominatif ; Second compte et transfert refusés |
| initial-administration / 25 | [Exception liée au compte actif](../../specs/initial-administration/spec.md#L25) | ND | Privilège permanent du compte actif |
| initial-administration / 34 | [Absence de MFA obligatoire au démarrage et au secours](../../specs/initial-administration/spec.md#L34) | ND | Premier démarrage sans MFA ; Réactivation de secours sans MFA |
| initial-administration / 49 | [Modes de démarrage explicites](../../specs/initial-administration/spec.md#L49) | ND | Marqueur externe indisponible |
| initial-administration / 63 | [Première configuration et transitions de mode](../../specs/initial-administration/spec.md#L63) | ND | État initial en base distinct du marqueur |
| initial-administration / 75 | [Provisionnement interactif de la base](../../specs/initial-administration/spec.md#L75) | ND | Base migrable |
| initial-administration / 90 | [Reprise et références de secrets après provisionnement](../../specs/initial-administration/spec.md#L90) | ND | Référence de secret après provisionnement |
| initial-administration / 105 | [Création conditionnelle du Super Admin](../../specs/initial-administration/spec.md#L105) | ND | Mots de passe différents ; Compte fonctionnel créé explicitement |
| initial-administration / 126 | [Réutilisation du Super Admin d'une base conservée](../../specs/initial-administration/spec.md#L126) | ND | Base conforme conservée |
| initial-administration / 136 | [Marqueur externe et première configuration](../../specs/initial-administration/spec.md#L136) | ND | Configuration initiale inachevée |
| initial-administration / 152 | [Panneau d'administration contrôlé](../../specs/initial-administration/spec.md#L152) | ND | Administrateur ordinaire soumis aux ACL |
| initial-administration / 165 | [Changement contrôlé de la route d'administration](../../specs/initial-administration/spec.md#L165) | ND | Ancienne route d'administration |
| initial-administration / 177 | [Expérience et état du panneau](../../specs/initial-administration/spec.md#L177) | ND | Santé réservée au root |
| initial-administration / 192 | [Désactivation externe du Super Admin](../../specs/initial-administration/spec.md#L192) | ND | Connexion root désactivée ; Secours malgré le marqueur de désactivation ; Transaction engagée lors de la désactivation |
| installation-provisioning / 9 | [Provisionnement du compte fonctionnel de secours](../../specs/installation-provisioning/spec.md#L9) | ND | Provisionnement sans compte nominatif ni MFA |
| installation-provisioning / 18 | [Provisionnement explicite et états inspectables](../../specs/installation-provisioning/spec.md#L18) | ND | Installation non provisionnée |
| installation-provisioning / 30 | [Configuration et secrets vérifiés avant mise en service](../../specs/installation-provisioning/spec.md#L30) | ND | Référence de secret indisponible |
| installation-provisioning / 42 | [Opérateur initial explicite et sans privilège implicite](../../specs/installation-provisioning/spec.md#L42) | ND | Identité opérateur absente |
| installation-provisioning / 55 | [Création tenant-scoped contrôlée](../../specs/installation-provisioning/spec.md#L55) | ND | Rejou du provisionnement du premier tenant |
| installation-provisioning / 68 | [Reprise contrôlée et auditée](../../specs/installation-provisioning/spec.md#L68) | ND | Interruption avant mise en service |
| internationalization / 8 | [Catalogues par composant et langue canonique](../../specs/internationalization/spec.md#L8) | P | Clé manquante bloquée |
| internationalization / 17 | [Résolution déterministe et formats localisés](../../specs/internationalization/spec.md#L17) | P | Valeur métier préservée ; Préférence navigateur avant défaut d'installation |
| security / 8 | [Exception applicative réservée au Super Admin](../../specs/security/spec.md#L8) | P | Revendication root sans authentification propre |
| security / 17 | [Profil de sécurité déclaré par composant](../../specs/security/spec.md#L17) | P | Vulnérabilité critique bloquante |
| security / 26 | [Échec fermé sans mode permissif](../../specs/security/spec.md#L26) | P | Contexte non vérifiable refusé |
| security / 37 | [Diagnostics sans exposition sensible](../../specs/security/spec.md#L37) | P | Secret hors journaux |
| themes / 8 | [Modes clair et sombre obligatoires](../../specs/themes/spec.md#L8) | P | Bascule sans rechargement |
| themes / 17 | [Tokens sémantiques sans valeurs codées](../../specs/themes/spec.md#L17) | P | Valeur codée rejetée |

## Empreintes SHA-256 du canon

- `openspec/specs/accessibility/spec.md` : `a3f9275d101b121d225c2975931a567b5ffed9d512ea22185bb28094e5821baf`.
- `openspec/specs/audit/spec.md` : `43d8dd9947fbac84c5decbf829825db577276853f5224e5bacc021c22bf4f513`.
- `openspec/specs/authorization-engine/spec.md` : `bd9de765f72d4700da314f81dbce9d3d0ee532f3bcc5be319f005ffbfd18b20b`.
- `openspec/specs/authorization/spec.md` : `87c9799579008033f39e47a579b8bf536f0d9c8973d678750a540a02ea63166f`.
- `openspec/specs/design-system/spec.md` : `c5ff33414eda8c66695366e189038db1f311f428e2e5e19b774907421131778e`.
- `openspec/specs/frontend/spec.md` : `e646e3faf793db109a93f803423cfa4606deeb67b91d4b3301fa219e82cf9414`.
- `openspec/specs/initial-administration/spec.md` : `200ce5a01e6d741d9021b2c78dd7f31efd7eeed566309168c0f3fbf468b5c4e5`.
- `openspec/specs/installation-provisioning/spec.md` : `2d33df47ef9ad0c073c4e0d7677c98e3cd96cb8e3b6866894c6d3cb7d305e7b4`.
- `openspec/specs/internationalization/spec.md` : `72a1a1756ae168e16d51055edeaa44786894caf20cc420c96ce9bb3da8907232`.
- `openspec/specs/security/spec.md` : `c033c6fa6a6fc43d6e7e3295cd7dc7f554bbcbe0c12cb9baf0431acd6f7a685f`.
- `openspec/specs/themes/spec.md` : `bd2008d3546647c84d913397230724ca1c48d3aac6ad3b4c509550ddbca6fb64`.

## Critère d’application du profil

Le rôle ou la capacité doit être effectivement sélectionné pour revendiquer sa garantie. Les exigences transversales d’identité, d’autorisation, d’audit, de gouvernance et de reprise demeurent applicables aux fonctions réellement livrées. Aucun statut de la matrice ne vaut verdict fonctionnel actuel.
