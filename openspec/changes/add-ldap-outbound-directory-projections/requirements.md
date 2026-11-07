# Références normatives — O08

<!-- ACL-PIXS-2026-10-31-E3-R1:start -->
## Références courantes du périmètre validé

Les copies plus anciennes conservées dans ce fichier sont historiques. Seuls les blocs ci-dessous correspondent au référentiel de la cible consolidée. Ils ne sont pas des deltas à synchroniser et ne prouvent aucune implémentation.

| Capacité | Exigence | Scénarios | Référence |
|---|---|---:|---|
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
| testing | Conformité des projections d'annuaire optionnelles | 1 | testing-6604920280fd |
| auth-managed-directory | LZT obligatoire par Domaine et exploitation PA | 1 | auth-managed-directory-64a5450351f4 |
| auth-managed-directory | PG source Core et LDAP opérationnel | 1 | auth-managed-directory-688b9c49db89 |
| auth-managed-directory | Référence PG et état opérationnel Kerberos normal | 2 | auth-managed-directory-ed0cb32e6d2f |
| auth-managed-directory | Multi-maître et convergence observable | 1 | auth-managed-directory-165383502bbf |
| auth-managed-directory | Authentification LDAP déléguée à Auth | 2 | auth-managed-directory-e24ef174b3d2 |
| auth-managed-directory | Réintégration contrôlée des annuaires | 1 | auth-managed-directory-a84e1bc47d92 |

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

### Référence courante testing-6604920280fd

Source : [testing](../../specs/testing/spec.md), ligne 75. SHA-256 : `6604920280fdee4ad9e71d6cef9d6576c30c1fa5efa9ba06157d6f7d21745c65`.

Scénarios : Repli conforme sans élargissement de droits.

~~~~text
### Requirement: Conformité des projections d'annuaire optionnelles

Les suites de conformité MUST vérifier le mapping versionné, la projection
sortante idempotente, la reprise, les suppressions propagées, l'isolation de
tenant et de scope, la fraîcheur après mutation, le repli PostgreSQL et l'état
DEGRADED d'un provider LDAP indisponible. Elles MUST vérifier que LDAP ne peut
ni écrire dans Pixs, ni fournir une ACL, une décision d'autorisation, une
révocation ou une authentification par cette capacité.

#### Scenario: Repli conforme sans élargissement de droits

- **WHEN** LDAP devient indisponible pendant une consultation autorisée
- **THEN** la suite confirme la réponse PostgreSQL, l'état DEGRADED et l'absence de divulgation ou de droit supplémentaire
~~~~

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
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| directory-projections / 11 | [Périmètre des ressources projetées](../../specs/directory-projections/spec.md#L11) | NE | AUDIT_AVANT_CREATION |
| directory-projections / 21 | [Autorité PostgreSQL des primitives Core](../../specs/directory-projections/spec.md#L21) | NE | AUDIT_AVANT_CREATION |
| directory-projections / 31 | [LDAP sans autorité ni écriture métier](../../specs/directory-projections/spec.md#L31) | NE | AUDIT_AVANT_CREATION |
| directory-projections / 41 | [Fonctions de sécurité exclues de la projection](../../specs/directory-projections/spec.md#L41) | NE | AUDIT_AVANT_CREATION |
| directory-projections / 51 | [Provider et mapping de projection déclarés](../../specs/directory-projections/spec.md#L51) | NE | AUDIT_AVANT_CREATION |
| directory-projections / 66 | [Projection sortante après mutation confirmée](../../specs/directory-projections/spec.md#L66) | NE | AUDIT_AVANT_CREATION |
| directory-projections / 77 | [Convergence reprenable et idempotente](../../specs/directory-projections/spec.md#L77) | NE | AUDIT_AVANT_CREATION |
| directory-projections / 87 | [Retard et retrait de projection observables](../../specs/directory-projections/spec.md#L87) | NE | AUDIT_AVANT_CREATION |
| testing / 75 | [Conformité des projections d'annuaire optionnelles](../../specs/testing/spec.md#L75) | P | COMPLETER_OU_INTEGRER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence directory-projections--c5293cebe9

Source : `openspec/specs/directory-projections/spec.md`, ligne 11. SHA-256 du bloc : `aa69fc04f4731210d55825392169f1455e882669fc70fe42db696a087abcb4cf`.

~~~~text
### Requirement: Périmètre des ressources projetées

La projection d'annuaire MUST couvrir exclusivement les identités numériques,
groupes et appartenances de `pixs.core`.

#### Scenario: Ressource hors périmètre déclarée

- **WHEN** un provider de projection LDAP déclare une ressource autre qu'une identité numérique, un groupe ou une appartenance de `pixs.core`
- **THEN** son activation est refusée avant toute synchronisation
~~~~

### Référence directory-projections--293a302d09

Source : `openspec/specs/directory-projections/spec.md`, ligne 21. SHA-256 du bloc : `8783b8ff3dd28bad646992a4de9ee1c7560a4e89b2fa14fce57d6cd60dc05435`.

~~~~text
### Requirement: Autorité PostgreSQL des primitives Core

PostgreSQL MUST rester la source de vérité ; toute création, modification,
révocation ou suppression MUST être décidée par une Command Pixs autorisée.

#### Scenario: Mutation Core demandée

- **WHEN** une création, modification, révocation ou suppression d'une primitive Core est demandée
- **THEN** une Command Pixs autorisée décide la mutation avant son éligibilité à la projection
~~~~

### Référence directory-projections--f09eb39c2a

Source : `openspec/specs/directory-projections/spec.md`, ligne 31. SHA-256 du bloc : `0a5e56873e10cfbcb516a6fb28b9a2500bca22547d844dec4a1278ce3fa95c23`.

~~~~text
### Requirement: LDAP sans autorité ni écriture métier

LDAP MUST NOT devenir une source d'autorité, accepter une écriture métier ni
importer un changement vers les primitives Core.

#### Scenario: Écriture LDAP refusée

- **WHEN** une modification d'identité, de groupe ou d'appartenance est détectée dans LDAP
- **THEN** elle n'est pas importée vers Pixs et un diagnostic auditable signale la divergence
~~~~

### Référence directory-projections--58d4e99552

Source : `openspec/specs/directory-projections/spec.md`, ligne 41. SHA-256 du bloc : `333f8ef16707254f9cf92748429d487c746fec1adc32fba2d2939e0d60e99c9b`.

~~~~text
### Requirement: Fonctions de sécurité exclues de la projection

Les ACL, permissions, décisions d'autorisation, authentification et mécanismes
de révocation MUST NOT être délégués à cette projection.

#### Scenario: Fonction de sécurité déléguée à LDAP

- **WHEN** un provider de projection LDAP déclare fournir une ACL, une permission, une décision d'autorisation, une authentification ou une révocation
- **THEN** il n'est pas sélectionné pour cette fonction et la composition est refusée
~~~~

### Référence directory-projections--e4f86bd02e

Source : `openspec/specs/directory-projections/spec.md`, ligne 51. SHA-256 du bloc : `95b260fa2dd6cadbb457efced15e88ebb4f62c35ef97af1d1c03660c27c9fbd4`.

~~~~text
### Requirement: Provider et mapping de projection déclarés

Un provider de projection LDAP MUST déclarer sa version de contrat, les
ressources projetées, les tenants et scopes admissibles, les attributs
autorisés, son mapping versionné et ses limites de fraîcheur. Les identifiants
internes Pixs MUST rester stables et le DN LDAP ainsi que tout identifiant
externe MUST rester des mappings du provider, jamais des identifiants
canoniques. Une donnée sans profil de gouvernance ou hors périmètre MUST NOT
être projetée.

#### Scenario: Mapping incomplet bloqué

- **WHEN** un provider LDAP déclare une ressource sans mapping versionné ou sans périmètre autorisé
- **THEN** son activation est refusée avant toute synchronisation
~~~~

### Référence directory-projections--035a0d26f7

Source : `openspec/specs/directory-projections/spec.md`, ligne 66. SHA-256 du bloc : `33d1a6ea87dd4a160b82cd4a559cd6a0818f291a88575ca243113a5958db832a`.

~~~~text
### Requirement: Projection sortante après mutation confirmée

La projection MUST être sortante depuis PostgreSQL. Une modification confirmée
de la source de vérité MUST être rendue éligible à la projection sans
transaction distribuée.

#### Scenario: Mutation confirmée éligible à la projection

- **WHEN** une modification est confirmée dans PostgreSQL
- **THEN** elle est rendue éligible à la projection sortante sans transaction distribuée
~~~~

### Référence directory-projections--385a3616eb

Source : `openspec/specs/directory-projections/spec.md`, ligne 77. SHA-256 du bloc : `720b2a1a183f0b7fd5c93555af55bf1572c1ef05309e0af03cbf70fd2967e361`.

~~~~text
### Requirement: Convergence reprenable et idempotente

La projection MUST disposer de checkpoints, versions, suppression ou tombstone,
retries bornés et rejeu idempotent persistants.

#### Scenario: Reprise après indisponibilité LDAP

- **WHEN** LDAP redevient disponible après une interruption de synchronisation
- **THEN** la projection reprend depuis son checkpoint sans créer de doublon ni réintroduire une donnée retirée
~~~~

### Référence directory-projections--fbc553732a

Source : `openspec/specs/directory-projections/spec.md`, ligne 87. SHA-256 du bloc : `10b912ec64f7f0f4402de0580c64a57cfbcef5b4630a187de712cb12be2fbfba`.

~~~~text
### Requirement: Retard et retrait de projection observables

L'état de convergence et tout retard MUST être observables. Une suppression,
révocation ou perte de visibilité autorisée dans Pixs MUST entraîner la mise à
jour ou le retrait correspondant de la projection selon sa politique déclarée.

#### Scenario: Perte de visibilité autorisée

- **WHEN** une identité numérique, un groupe ou une appartenance perd une visibilité autorisée dans Pixs
- **THEN** la projection est mise à jour ou retirée conformément à sa politique déclarée
~~~~

### Référence testing--19ab684105

Source : `openspec/specs/testing/spec.md`, ligne 75. SHA-256 du bloc : `4d1c7c58c3080d486f81efcd997cab6ade6c991c51d056d9ea8daa81ef6f6fa5`.

~~~~text
### Requirement: Conformité des projections d'annuaire optionnelles

Les suites de conformité MUST vérifier le mapping versionné, la projection
sortante idempotente, la reprise, les suppressions propagées, l'isolation de
tenant et de scope, la fraîcheur après mutation, le repli PostgreSQL et l'état
DEGRADED d'un provider LDAP indisponible. Elles MUST vérifier que LDAP ne peut
ni écrire dans Pixs, ni fournir une ACL, une décision d'autorisation, une
révocation ou une authentification par cette capacité.

#### Scenario: Repli conforme sans élargissement de droits

- **WHEN** LDAP devient indisponible pendant une consultation autorisée
- **THEN** la suite confirme la réponse PostgreSQL, l'état DEGRADED et l'absence de divulgation ou de droit supplémentaire
~~~~

