# Références normatives — add-auth-managed-openldap

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Références courantes du périmètre validé

Les copies plus anciennes conservées dans ce fichier sont historiques. Seuls les blocs ci-dessous correspondent au référentiel de la cible consolidée. Ils ne sont pas des deltas à synchroniser et ne prouvent aucune implémentation.

| Capacité | Exigence | Scénarios | Référence |
|---|---|---:|---|
| auth-managed-directory | LZT obligatoire par Domaine et exploitation PA | 1 | auth-managed-directory-64a5450351f4 |
| auth-managed-directory | PG source Core et LDAP opérationnel | 1 | auth-managed-directory-688b9c49db89 |
| auth-managed-directory | Référence PG et état opérationnel Kerberos normal | 2 | auth-managed-directory-ed0cb32e6d2f |
| auth-managed-directory | Multi-maître et convergence observable | 1 | auth-managed-directory-165383502bbf |
| auth-managed-directory | Authentification LDAP déléguée à Auth | 2 | auth-managed-directory-e24ef174b3d2 |
| auth-managed-directory | Réintégration contrôlée des annuaires | 1 | auth-managed-directory-a84e1bc47d92 |
| directory-projections | Périmètre des ressources projetées | 1 | directory-projections-39056c5e399f |
| directory-projections | Autorité PostgreSQL des primitives Core | 1 | directory-projections-d8686e6ffbe2 |
| directory-projections | LDAP sans autorité ni écriture métier | 1 | directory-projections-3f9464f4589d |
| directory-projections | Fonctions de sécurité exclues de la projection | 1 | directory-projections-78e8d5eb9c1b |
| directory-projections | Provider et mapping de projection déclarés | 1 | directory-projections-0a40b264ab89 |
| directory-projections | Projection sortante après mutation confirmée | 1 | directory-projections-3ed6dcf50711 |
| directory-projections | Convergence reprenable et idempotente | 1 | directory-projections-3e75cb3b852e |
| directory-projections | Retard et retrait de projection observables | 1 | directory-projections-3910cb95ee02 |
| directory-projections | Consultation avec préférence LDAP et repli PostgreSQL | 1 | directory-projections-b9064ba82b2e |
| directory-projections | Fraîcheur après mutation et cohérence de lecture | 1 | directory-projections-64bd3e217d3f |
| directory-projections | Autorisation et confidentialité préservées à la consultation | 1 | directory-projections-88316b878b5c |
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

### Référence courante auth-managed-directory-64a5450351f4

Source : [auth-managed-directory](../../specs/auth-managed-directory/spec.md), ligne 11. SHA-256 : `64a5450351f4ce0ffad443f7e8e42dd73e5810d8a4a2cbbfa83e618a3dbd2dd4`.

Scénarios : ZT partagé.

~~~~text
### Requirement: LZT obligatoire par Domaine et exploitation PA

Chaque Domaine MUST disposer d'au moins un LZT/OpenLDAP et MAY en redonder plusieurs. PA MUST installer, configurer et exploiter les services ; PBO/Core/Auth MUST administrer données, politiques et habilitations par leurs contrats publics. PZT MUST assurer le réseau sans appliquer la configuration OpenLDAP.

#### Scenario: ZT partagé

- **WHEN** deux Domaines partagent ZT
- **THEN** chacun conserve son annuaire et les exécutants PA requis sans fusion des données.
~~~~

### Référence courante auth-managed-directory-688b9c49db89

Source : [auth-managed-directory](../../specs/auth-managed-directory/spec.md), ligne 20. SHA-256 : `688b9c49db89d53dda98e5b2f81be5434a9736109f8d418e054f5e5c309b2f7b`.

Scénarios : Écriture divergente.

~~~~text
### Requirement: PG source Core et LDAP opérationnel

Les individus et identités numériques déclarées, groupes et ACL applicatifs MUST garder PG comme source de vérité. LZT MUST publier les identités/groupes autorisés pour consultation des applications. Les écritures directes LDAP MUST NOT remplacer les Commands Core ni être réimportées comme vérité métier ; les ACL techniques LDAP MUST rester distinctes des droits Pixs.

#### Scenario: Écriture divergente

- **WHEN** une entrée projetée est modifiée directement dans LDAP
- **THEN** la divergence est diagnostiquée sans mutation Core implicite.
~~~~

### Référence courante auth-managed-directory-ed0cb32e6d2f

Source : [auth-managed-directory](../../specs/auth-managed-directory/spec.md), ligne 29. SHA-256 : `ed0cb32e6d2f66d1e2fcb959e66aa1bb88470e4f9a2aa4b27e266ce3ba13f4a8`.

Scénarios : Publication normale; Perte totale des annuaires.

~~~~text
### Requirement: Référence PG et état opérationnel Kerberos normal

PG MUST rester souveraine pour les individus, identités déclarées, groupes, ACL et configurations Pixs. En fonctionnement normal, l'état Kerberos durable MUST résider dans LDAP et la publication PG MUST préserver principals, clés et états natifs. La reconstruction complète depuis PG MUST être une procédure d'urgence en mode critique selon auth-managed-kerberos, sans exiger le déplacement des écritures natives normales vers PG.

#### Scenario: Publication normale

- **WHEN** Core/Auth republient les références PG
- **THEN** les données natives Kerberos présentes dans LDAP restent préservées.

#### Scenario: Perte totale des annuaires

- **WHEN** le Domaine déclenche une reconstruction complète
- **THEN** il suit la procédure critique déclarée sans présenter PG seule comme copie courante de toutes les clés Kerberos.
~~~~

### Référence courante auth-managed-directory-165383502bbf

Source : [auth-managed-directory](../../specs/auth-managed-directory/spec.md), ligne 43. SHA-256 : `165383502bbf45a4ca2107794551b3c1fe18c0807fc553fd7b404c17009ed21f`.

Scénarios : Publication en retard.

~~~~text
### Requirement: Multi-maître et convergence observable

Les LZT d'un Domaine MUST pouvoir fonctionner en multi-maître avec réplication propre à LDAP, protections de transport, règles explicites de concurrence, conflits et partition. La confirmation PG MUST NOT valoir convergence LDAP et le multi-maître LDAP MUST NOT modifier l'unicité du primaire PG.

#### Scenario: Publication en retard

- **WHEN** une modification PG est confirmée sans convergence d’un LZT
- **THEN** son retard reste visible et les fonctions exigeant cet état n’annoncent pas une mise à jour effective.
~~~~

### Référence courante auth-managed-directory-e24ef174b3d2

Source : [auth-managed-directory](../../specs/auth-managed-directory/spec.md), ligne 52. SHA-256 : `e24ef174b3d20b2fa7126470c246286e7c0486510ca27133a8c2adfb9325bc44`.

Scénarios : Projection seule; Délégation indisponible.

~~~~text
### Requirement: Authentification LDAP déléguée à Auth

Les applications et identités explicitement autorisées MAY s'authentifier via LDAP sous profil Auth. La vérification MUST être déléguée à pixs.auth par un mécanisme qualifié, sur canaux protégés et avec verrouillage commun par identité. La seule projection MUST NOT fournir ce droit ou constituer un repli d'authentification implicite.

#### Scenario: Projection seule

- **WHEN** un profil ne sélectionne que la consultation LDAP
- **THEN** aucun bind d’authentification des individus n’est admis par cette seule sélection.

#### Scenario: Délégation indisponible

- **WHEN** la vérification Auth exigée n’est pas disponible
- **THEN** l’authentification concernée est refusée sans vérification locale moins exigeante.
~~~~

### Référence courante auth-managed-directory-a84e1bc47d92

Source : [auth-managed-directory](../../specs/auth-managed-directory/spec.md), ligne 66. SHA-256 : `a84e1bc47d923174f66fdf360480e0ac484cd02f994596115e88e85782d5184b`.

Scénarios : Ancienne copie LDAP.

~~~~text
### Requirement: Réintégration contrôlée des annuaires

Un LZT restauré ou en retard MUST réconcilier retraits, identités, état Kerberos et politiques courantes avant son admission aux services concernés. L'exclusion puis la réadmission MUST suivre le profil et ses preuves ; une ancienne copie MUST NOT réintroduire un accès retiré.

#### Scenario: Ancienne copie LDAP

- **WHEN** la copie restaurée contient un compte révoqué
- **THEN** elle ne traite pas les authentifications concernées avant réconciliation vérifiée.
~~~~

### Référence courante directory-projections-39056c5e399f

Source : [directory-projections](../../specs/directory-projections/spec.md), ligne 11. SHA-256 : `39056c5e399f47dff6366b8502f99a2b0e01fdcc51bf69c2dceaa1dee68111eb`.

Scénarios : Ressource hors périmètre déclarée.

~~~~text
### Requirement: Périmètre des ressources projetées

La projection d'annuaire MUST couvrir exclusivement les identités numériques,
groupes et appartenances de `pixs.core`.

#### Scenario: Ressource hors périmètre déclarée

- **WHEN** un provider de projection LDAP déclare une ressource autre qu'une identité numérique, un groupe ou une appartenance de `pixs.core`
- **THEN** son activation est refusée avant toute synchronisation
~~~~

### Référence courante directory-projections-d8686e6ffbe2

Source : [directory-projections](../../specs/directory-projections/spec.md), ligne 21. SHA-256 : `d8686e6ffbe288cf4255715ec24a02b708145edf035262b888c960e4bb87ea48`.

Scénarios : Mutation Core demandée.

~~~~text
### Requirement: Autorité PostgreSQL des primitives Core

PostgreSQL MUST rester la source de vérité ; toute création, modification,
révocation ou suppression MUST être décidée par une Command Pixs autorisée.

#### Scenario: Mutation Core demandée

- **WHEN** une création, modification, révocation ou suppression d'une primitive Core est demandée
- **THEN** une Command Pixs autorisée décide la mutation avant son éligibilité à la projection
~~~~

### Référence courante directory-projections-3f9464f4589d

Source : [directory-projections](../../specs/directory-projections/spec.md), ligne 31. SHA-256 : `3f9464f4589d99b2d027fa53753aa0f570d729b60e47e38744e9f7e545c0890c`.

Scénarios : Écriture LDAP refusée.

~~~~text
### Requirement: LDAP sans autorité ni écriture métier

La projection LDAP MUST NOT devenir source Core ni importer une écriture LDAP comme vérité métier. L'état opérationnel Kerberos durable normal MUST être géré dans LDAP par ses mécanismes autorisés et rester distinct des données Core projetées. La publication PG MUST le préserver et sa présence MUST NOT constituer une divergence Core. La reconstruction critique MUST suivre auth-managed-kerberos.

#### Scenario: Écriture LDAP refusée

- **WHEN** une entrée Core projetée est modifiée directement hors Command
- **THEN** elle n’est pas importée et la divergence est signalée.
~~~~

### Référence courante directory-projections-78e8d5eb9c1b

Source : [directory-projections](../../specs/directory-projections/spec.md), ligne 40. SHA-256 : `78e8d5eb9c1bd374941b5ca869e1599cf9062ef7ee0e4a61fe634c53edffe4a8`.

Scénarios : Fonction non sélectionnée.

~~~~text
### Requirement: Fonctions de sécurité exclues de la projection

La projection seule MUST NOT fournir authentification, décisions d'autorisation ou ACL applicatives. Le service LDAP MUST pouvoir fournir séparément les fonctions autorisées par auth-managed-directory et auth-managed-kerberos, avec habilitations et protection distinctes. Un repli de consultation MUST NOT activer une méthode d'authentification.

#### Scenario: Fonction non sélectionnée

- **WHEN** la seule capacité de projection est invoquée pour vérifier un mot de passe
- **THEN** la demande est refusée sans droit d’authentification déduit.
~~~~

### Référence courante directory-projections-0a40b264ab89

Source : [directory-projections](../../specs/directory-projections/spec.md), ligne 49. SHA-256 : `0a40b264ab89fffc599188b3ca8bf0995a9f5e7801265c35e424f5e46d456de2`.

Scénarios : Mapping incomplet bloqué.

~~~~text
### Requirement: Provider et mapping de projection déclarés

Le provider MUST déclarer version, ressources, Instance/Domaine/tenants/scopes admissibles, attributs, mapping et fraîcheur. Les UUID Core MUST rester stables ; DN et identifiants externes MUST rester des mappings. Données non classifiées et périmètres non autorisés MUST NOT être exportés. La disponibilité de LZT MUST suivre les minima Domaine sans rendre tout connecteur externe obligatoire.

#### Scenario: Mapping incomplet bloqué

- **WHEN** une ressource ne possède pas son mapping ou périmètre autorisé
- **THEN** sa projection est bloquée avant effet.
~~~~

### Référence courante directory-projections-3ed6dcf50711

Source : [directory-projections](../../specs/directory-projections/spec.md), ligne 58. SHA-256 : `3ed6dcf50711b481d2518e10f38d4d35d99947af46c23714098f309167c8152d`.

Scénarios : Mutation confirmée éligible à la projection.

~~~~text
### Requirement: Projection sortante après mutation confirmée

La projection MUST être sortante depuis PostgreSQL. Une modification confirmée
de la source de vérité MUST être rendue éligible à la projection sans
transaction distribuée.

#### Scenario: Mutation confirmée éligible à la projection

- **WHEN** une modification est confirmée dans PostgreSQL
- **THEN** elle est rendue éligible à la projection sortante sans transaction distribuée
~~~~

### Référence courante directory-projections-3e75cb3b852e

Source : [directory-projections](../../specs/directory-projections/spec.md), ligne 69. SHA-256 : `3e75cb3b852ea8a14cbec32566e8318710d08fdf9d54e12a4b8ef07497b7cf93`.

Scénarios : Reprise après indisponibilité LDAP.

~~~~text
### Requirement: Convergence reprenable et idempotente

La projection MUST disposer de checkpoints, versions, suppression ou tombstone,
retries bornés et rejeu idempotent persistants.

#### Scenario: Reprise après indisponibilité LDAP

- **WHEN** LDAP redevient disponible après une interruption de synchronisation
- **THEN** la projection reprend depuis son checkpoint sans créer de doublon ni réintroduire une donnée retirée
~~~~

### Référence courante directory-projections-3910cb95ee02

Source : [directory-projections](../../specs/directory-projections/spec.md), ligne 79. SHA-256 : `3910cb95ee02e30573151652f08071bb0f3c7231ff33d5e421abbb9ae3eca994`.

Scénarios : Perte de visibilité autorisée.

~~~~text
### Requirement: Retard et retrait de projection observables

L'état de convergence et tout retard MUST être observables. Une suppression,
révocation ou perte de visibilité autorisée dans Pixs MUST entraîner la mise à
jour ou le retrait correspondant de la projection selon sa politique déclarée.

#### Scenario: Perte de visibilité autorisée

- **WHEN** une identité numérique, un groupe ou une appartenance perd une visibilité autorisée dans Pixs
- **THEN** la projection est mise à jour ou retirée conformément à sa politique déclarée
~~~~

### Référence courante directory-projections-b9064ba82b2e

Source : [directory-projections](../../specs/directory-projections/spec.md), ligne 90. SHA-256 : `b9064ba82b2efa6ce8ee07a0675932d02901142827857b34869efbb9e9c4fd41`.

Scénarios : LDAP indisponible.

~~~~text
### Requirement: Consultation avec préférence LDAP et repli PostgreSQL

Le contrat de consultation des identités numériques, groupes et appartenances
MUST utiliser LDAP seulement lorsqu'un provider explicitement sélectionné est
disponible et dans sa limite de fraîcheur déclarée. Lorsque LDAP est
injoignable, non conforme ou hors de cette limite, la consultation MUST lire
PostgreSQL, exposer l'état DEGRADED et produire un diagnostic corrélé. Le
service MUST NOT présenter silencieusement une réponse LDAP périmée comme une
lecture de référence.

#### Scenario: LDAP indisponible

- **WHEN** le provider LDAP sélectionné ne peut pas être joint
- **THEN** la consultation autorisée est servie par PostgreSQL et la projection passe à l'état DEGRADED diagnostiquable
~~~~

### Référence courante directory-projections-64bd3e217d3f

Source : [directory-projections](../../specs/directory-projections/spec.md), ligne 105. SHA-256 : `64bd3e217d3f2d001489a4fe78c51598c6675dd336d08e23ba32e70fd9f65bc4`.

Scénarios : Lecture après changement de groupe.

~~~~text
### Requirement: Fraîcheur après mutation et cohérence de lecture

Après une mutation confirmée dans PostgreSQL, le contrat de consultation MUST
privilégier PostgreSQL jusqu'à la convergence LDAP ou refuser explicitement la
lecture LDAP tant que la garantie de fraîcheur déclarée n'est pas satisfaite.
La sélection de source MUST être déterministe pour un même contexte et MUST
NOT dépendre de l'ordre des requêtes ou de l'état d'un cache local.

#### Scenario: Lecture après changement de groupe

- **WHEN** une appartenance à un groupe est modifiée et que LDAP n'a pas encore confirmé la projection
- **THEN** la consultation renvoie l'état PostgreSQL confirmé au lieu de l'ancienne projection LDAP
~~~~

### Référence courante directory-projections-88316b878b5c

Source : [directory-projections](../../specs/directory-projections/spec.md), ligne 118. SHA-256 : `88316b878b5cf270b173aa29d5413aba9e09f4dd6824bf202f7e67e98cfcca82`.

Scénarios : Consultation hors tenant refusée.

~~~~text
### Requirement: Autorisation et confidentialité préservées à la consultation

Toute consultation, qu'elle lise LDAP ou PostgreSQL, MUST être autorisée et
filtrée par Pixs avec le tenant, le ScopeContext et les permissions canoniques.
LDAP MUST NOT devenir un moteur de décision, une source de révocation ou un
contournement des ACL. Les diagnostics, mappings et erreurs MUST NOT exposer de
credential, DN non autorisé, donnée personnelle ou existence d'une ressource
hors périmètre.

#### Scenario: Consultation hors tenant refusée

- **WHEN** un appelant tente de consulter une identité ou un groupe hors de son périmètre
- **THEN** Pixs refuse la demande avant toute divulgation provenant de LDAP ou de PostgreSQL
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
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

## Statut des deltas antérieurs après contrôle E3

Les anciens fichiers sous specs/ ont été déplacés, avec empreintes conservées, vers [l’historique interne](historique-deltas-avant-e3/README.md). Le [contrôle de couverture](COUVERTURE_DELTAS_E3.md) relie chaque ancienne exigence au contrat courant et aux tâches ouvertes. Le dossier reste actif ; skip_specs évite seulement la réapplication des anciennes prescriptions. Il ne termine ni la réalisation, ni les tests, ni les 49 tâches encore ouvertes dans les sept dossiers concernés.
