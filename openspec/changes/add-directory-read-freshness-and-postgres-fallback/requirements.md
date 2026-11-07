# Références normatives — O09

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
| authentication | Fournisseurs déclarés et confiance explicite | 1 | authentication-19f40b972c78 |
| authentication | Identifiant externe canonique et liaison explicite | 1 | authentication-cf3b90403a1e |
| authentication | Sessions bornées et révocation propagée | 2 | authentication-bba360459f9c |
| authentication | Module essentiel autonome pixs.auth | 2 | authentication-2cd9fc78aed8 |
| authentication | Autonomie locale et PostgreSQL par défaut | 3 | authentication-7deab703128c |
| authentication | Propriété des données Auth et protection des justificatifs | 2 | authentication-5af8eb52988f |
| authentication | Sous-modules Auth composés par les mécanismes communs | 1 | authentication-f8a9e9da127b |
| authentication | Politiques Auth déclaratives et contextualisées | 1 | authentication-2a10fbff7239 |
| authentication | Absence de repli implicite entre méthodes et sources | 2 | authentication-64ed6a16a8f6 |
| authentication | Interfaces spécialisées du profil Auth local | 1 | authentication-ca439766ea7f |
| authentication | Justificatifs opaques et stockage serveur par empreinte | 1 | authentication-c43dd24e0955 |
| authentication | État Auth courant requis | 1 | authentication-fb37fa48763a |
| authentication | Durées des sessions locales ordinaires | 2 | authentication-f58a4b2bf783 |
| authentication | Durée des accès et fraîcheur sensible | 2 | authentication-81737f3de29d |
| authentication | Politique configurable et exceptions canoniques | 1 | authentication-f87c04c0556b |
| authentication | Renouvellement rotatif à usage unique | 1 | authentication-9f0d9b2938e0 |
| authentication | Activité utilisateur et renouvellement | 1 | authentication-c668081af427 |
| authentication | Concurrence et réponse perdue de rotation | 2 | authentication-d9131b3941bf |
| authentication | Réutilisation suspecte et révocation de session | 1 | authentication-4cc4a81801fe |
| authentication | Plafond et remplacement explicite des sessions | 2 | authentication-42558d8e901e |
| authentication | Onglets et renouvellements sans nouvelle session | 1 | authentication-3f508363903c |
| authentication | Changement de mot de passe sans reconnexion automatique | 2 | authentication-1f281505aa1c |
| authentication | Récupération et compromission du mot de passe | 2 | authentication-7e9531288ce6 |
| authentication | Argon2id via les outils Django | 1 | authentication-2e7a00ac3949 |
| authentication | Réutilisation Argon2id dans un profil OpenLDAP qualifié | 2 | authentication-82591f961338 |
| authentication | Limites de la compatibilité des empreintes | 1 | authentication-882a416b3157 |
| authentication | Conservation du renouvellement de la CLI interactive | 1 | authentication-38870e5fe1b2 |
| authentication | Mot de passe commun par identité numérique | 1 | authentication-c423b942ab64 |
| authentication | Changement uniquement depuis PBO | 1 | authentication-29ea6c6bc11d |
| authentication | Récupération configurable et désactivée par défaut | 1 | authentication-7507cdda1859 |
| authentication | MFA choisie par profil et chemins qualifiés | 1 | authentication-d40c9ae62ea3 |
| authentication | Changements effectifs et contrôleurs à jour | 1 | authentication-d30f23cea222 |
| authentication | Verrouillage commun et états dépendants | 1 | authentication-19aff870d368 |

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

### Référence courante authentication-19f40b972c78

Source : [authentication](../../specs/authentication/spec.md), ligne 8. SHA-256 : `19f40b972c7847934dfd3652c5fc9dc435a200f49ca6ba0194190f7e8f0a7b14`.

Scénarios : Émetteur non approuvé refusé.

~~~~text
### Requirement: Fournisseurs déclarés et confiance explicite

Chaque fournisseur (local, OIDC, SAML) MUST déclarer protocole, émetteurs, audiences, algorithmes, clés, claims obligatoires et mappings ; la seule validité cryptographique MUST NOT suffire sans confiance applicative configurée.

#### Scenario: Émetteur non approuvé refusé

- **WHEN** un jeton valide émane d'un émetteur non approuvé
- **THEN** l'authentification est refusée avec une erreur stable et un audit
~~~~

### Référence courante authentication-cf3b90403a1e

Source : [authentication](../../specs/authentication/spec.md), ligne 17. SHA-256 : `cf3b90403a1e4309fe5f284e5b5d57dc277f4951d68d4dfd85a8a122409fedea`.

Scénarios : Courriel seul non rapproché.

~~~~text
### Requirement: Identifiant externe canonique et liaison explicite

Le système MUST respecter les garanties suivantes.

L'identifiant externe canonique est le triplet fournisseur, émetteur, sujet ; toute liaison à une identité existante est explicite, vérifiée des deux côtés, idempotente et auditée ; aucun rapprochement par courriel seul.

#### Scenario: Courriel seul non rapproché

- **WHEN** deux comptes partagent la même adresse sans preuve bilatérale
- **THEN** aucune fusion n'a lieu et une liaison explicite reste exigée
~~~~

### Référence courante authentication-bba360459f9c

Source : [authentication](../../specs/authentication/spec.md), ligne 28. SHA-256 : `bba360459f9c54d5266d275f5e1cc8690b32e4ca5436162d1d01e8fc54f75db5`.

Scénarios : Révocation propagée; Retrait sans audit confirmé.

~~~~text
### Requirement: Sessions bornées et révocation propagée

Sessions, jetons et renouvellements MUST être bornés et rotatifs, avec détection de réutilisation. Toute révocation d’identité, justificatif, session ou confiance MUST invalider les contextes concernés sans supprimer les données métier. L’audit MUST suivre audit, sans secret, avec son exception limitée au retrait d’accès Auth. Révocation persistante et audit réussi MUST NOT être annoncés sans leur preuve.

#### Scenario: Révocation propagée
- **WHEN** une identité ou une session est révoquée
- **THEN** les contextes dérivés sont invalidés avant toute nouvelle opération sensible

#### Scenario: Retrait sans audit confirmé
- **WHEN** seul l’audit est indisponible et qu’un retrait d’accès Auth autorisé est persisté selon l’exception dédiée
- **THEN** les contextes concernés sont invalidés et l’échec d’audit reste signalé pour réconciliation sans audit fictif
~~~~

### Référence courante authentication-2cd9fc78aed8

Source : [authentication](../../specs/authentication/spec.md), ligne 40. SHA-256 : `2cd9fc78aed8a023b789605bbbbd7de954d34a3dd3addaa5bf144945f18e405a`.

Scénarios : Composition applicative sans Auth; Fixture structurelle isolée.

~~~~text
### Requirement: Module essentiel autonome pixs.auth

Toute composition applicative Pixs MUST inclure `pixs.auth`, module essentiel indépendant de `pixs.core`, avec une capacité locale autonome sélectionnée explicitement par le profil. Son absence MUST empêcher l'activation applicative. Les fixtures structurelles non applicatives MUST rester distinguées de ce profil.

#### Scenario: Composition applicative sans Auth
- **WHEN** une composition applicative omet pixs.auth ou sa capacité locale requise
- **THEN** sa validation échoue avant activation sans annoncer d'authentification disponible

#### Scenario: Fixture structurelle isolée
- **WHEN** un test manipule seulement un contrat pur Core sans runtime applicatif
- **THEN** il reste possible sans Auth et ne constitue pas une composition applicative qualifiée
~~~~

### Référence courante authentication-7deab703128c

Source : [authentication](../../specs/authentication/spec.md), ligne 52. SHA-256 : `7deab703128c58f53bf986cc8aa083c34d13801b0c7b28ec2dfbcc7702a73096`.

Scénarios : Installation autonome; Authentification PG Domaine; État PG courant absent.

~~~~text
### Requirement: Autonomie locale et PostgreSQL par défaut

Avant le premier Domaine, Auth MUST pouvoir authentifier sur PG Instance sans fournisseur externe, LDAP/KDC ni Internet. Après activation, les identités MUST appartenir aux Domaines et PG Instance MUST NOT conserver d'identité numérique d'Instance. Auth MAY authentifier directement sur PG Domaine sous profil explicite et qualifié ; LZT/KZT MUST rester obligatoires par Domaine sans imposer leur disponibilité à ce chemin PG autorisé.

#### Scenario: Installation autonome

- **WHEN** le profil pré-domaine local est sélectionné
- **THEN** l’authentification PG Instance reste possible selon ses moyens et politiques.

#### Scenario: Authentification PG Domaine

- **WHEN** un profil permet explicitement PG Domaine avec ses garanties
- **THEN** Auth utilise l’identité de Domaine sans réactiver son ancienne identité d’Instance.

#### Scenario: État PG courant absent

- **WHEN** l’opération exige une PG actuelle indisponible
- **THEN** elle échoue fermée sans fichier ou session supposée valide.
~~~~

### Référence courante authentication-5af8eb52988f

Source : [authentication](../../specs/authentication/spec.md), ligne 71. SHA-256 : `5af8eb52988f703d72691a1d8e5a01544fea517f7e2333a79cc63b9d612d8747`.

Scénarios : Session persistée; Liaison avec Core.

~~~~text
### Requirement: Propriété des données Auth et protection des justificatifs

pixs.auth MUST posséder ses justificatifs, liaisons d'authentification, politiques et sessions, rattachés aux identités Core par contrat public. Les mots de passe MUST être stockés uniquement sous empreinte sécurisée ; les jetons réutilisables, clés privées et secrets MFA MUST NOT être stockés en clair dans les tables métier, manifests ou journaux. Les secrets réversibles MUST suivre les contrats de protection et de secrets applicables.

#### Scenario: Session persistée
- **WHEN** Auth conserve une session ou un renouvellement
- **THEN** l'enregistrement permet expiration et révocation sans exposer le jeton brut réutilisable

#### Scenario: Liaison avec Core
- **WHEN** Auth rattache un moyen à une DigitalIdentity
- **THEN** la référence est vérifiée par contrat public sans écriture directe dans les tables Core
~~~~

### Référence courante authentication-f8a9e9da127b

Source : [authentication](../../specs/authentication/spec.md), ligne 83. SHA-256 : `f8a9e9da127b784472c0fc7d7aa9fd8ec4115e59069299b27a283b0d935580f4`.

Scénarios : Source installée sans confiance.

~~~~text
### Requirement: Sous-modules Auth composés par les mécanismes communs

Les méthodes locales, l'enrôlement, l'émission d'identité, les services gérés et les sources externes MUST être extensibles par composants déclarés et contrats versionnés. Les sous-modules MUST utiliser le manifest et le lifecycle communs sans registre parallèle. L'installation d'un sous-module MUST NOT suffire à activer une confiance ou un service.

#### Scenario: Source installée sans confiance
- **WHEN** un sous-module de source est installé sans configuration de confiance validée
- **THEN** il ne peut authentifier aucune identité
~~~~

### Référence courante authentication-2a10fbff7239

Source : [authentication](../../specs/authentication/spec.md), ligne 91. SHA-256 : `2a10fbff7239d37dc777e2035ab2d9daeed141895d618b15f1f822f95a53fb49`.

Scénarios : Politique contradictoire.

~~~~text
### Requirement: Politiques Auth déclaratives et contextualisées

Les politiques Auth MUST être typées, versionnées et résolues déterministiquement selon Instance, Domaine, profil et contexte tenant/scope applicable. Méthodes, MFA, fraîcheur, sessions, récupération et confiance MUST exposer origine et valeur effective sans secret. Une règle contradictoire MUST bloquer l'opération sans sélection opportuniste de la moins exigeante.

#### Scenario: Politique contradictoire

- **WHEN** les règles ne permettent pas de déterminer l’assurance applicable
- **THEN** Auth refuse avec diagnostic sans réduire implicitement les exigences.
~~~~

### Référence courante authentication-64ed6a16a8f6

Source : [authentication](../../specs/authentication/spec.md), ligne 100. SHA-256 : `64ed6a16a8f6769d91ff1f258024246cb9de57963ce0c74565c58c91b30d91bc`.

Scénarios : IdP externe indisponible; Secours propre du Super Admin.

~~~~text
### Requirement: Absence de repli implicite entre méthodes et sources

Une indisponibilité externe MUST NOT activer une authentification locale ou diminuer l'assurance requise. La coexistence des sources et méthodes MUST suivre une politique explicite et préserver la liaison canonique. Le compte de secours MUST conserver son authentification propre et son exception selon authorization et initial-administration, sans extension aux comptes ordinaires.

#### Scenario: IdP externe indisponible
- **WHEN** une politique impose un IdP externe indisponible pour un compte ordinaire
- **THEN** un mot de passe local ne devient pas un repli autorisé par cette seule panne

#### Scenario: Secours propre du Super Admin
- **WHEN** le Super Admin utilise son parcours canonique de secours sans MFA
- **THEN** son exception reste applicable sans attribuer un niveau MULTI_FACTOR non obtenu
~~~~

### Référence courante authentication-ca439766ea7f

Source : [authentication](../../specs/authentication/spec.md), ligne 112. SHA-256 : `ca439766ea7fc07ebcabc2de93893796ead6e0a27c17ef7207c249d3de383b4a`.

Scénarios : Session liée à Core.

~~~~text
### Requirement: Interfaces spécialisées du profil Auth local

Le profil local MUST exposer des interfaces spécialisées d’authentification, de sessions et de justificatifs, typées et versionnées dans le même module pixs.auth. Les façades web, API et CLI MUST réutiliser ces contrats. Auth MUST référencer les identités Core par UUID et ports publics, posséder ses écritures et MUST NOT exposer de modèle Django privé ni écrire dans les tables privées d’un autre module.

#### Scenario: Session liée à Core
- **WHEN** une façade demande une session
- **THEN** Auth vérifie la référence et l’état Core par port public puis possède ses écritures, sans modèle privé exposé
~~~~

### Référence courante authentication-c43dd24e0955

Source : [authentication](../../specs/authentication/spec.md), ligne 120. SHA-256 : `c43dd24e0955878cdc29c3245ac9db762b0718920b26954272409fcda6fa5958`.

Scénarios : Justificatif brut absent.

~~~~text
### Requirement: Justificatifs opaques et stockage serveur par empreinte

Le profil local MUST utiliser des identifiants de session et jetons API/CLI opaques issus d’un générateur aléatoire cryptographiquement sûr. Les justificatifs remis au client MUST être conservés côté serveur uniquement sous empreinte de vérification, avec état, expiration et révocation dans PostgreSQL. Un backend conservant leur valeur brute MUST NOT être repris sans adaptation conforme.

#### Scenario: Justificatif brut absent
- **WHEN** Auth persiste une session ou un jeton
- **THEN** la vérification par empreinte et la révocation sont possibles sans stocker ni journaliser le justificatif brut réutilisable
~~~~

### Référence courante authentication-fb37fa48763a

Source : [authentication](../../specs/authentication/spec.md), ligne 128. SHA-256 : `fb37fa48763ac16ec2a80b11378e43f8da96b332bedb0e4a771f6fec35bda3b2`.

Scénarios : État inaccessible.

~~~~text
### Requirement: État Auth courant requis

Un contrôle nécessitant l’état Auth courant MUST échouer fermé si cet état ne peut pas être vérifié. PostgreSQL indisponible MUST NOT entraîner un repli vers un fichier ou un jeton supposé valide.

#### Scenario: État inaccessible
- **WHEN** PostgreSQL Auth ne permet pas de vérifier l’état courant requis
- **THEN** l’accès est refusé sans repli implicite
~~~~

### Référence courante authentication-f58a4b2bf783

Source : [authentication](../../specs/authentication/spec.md), ligne 136. SHA-256 : `f58a4b2bf78334507b530cf4d14f24b8b5ea14d5d6518292fa31f7c19ce74bfc`.

Scénarios : Inactivité ordinaire; Plafond administratif.

~~~~text
### Requirement: Durées des sessions locales ordinaires

Par défaut, les sessions ordinaires MUST expirer après 60 minutes d’inactivité ou 12 heures au total et les sessions d’administration ordinaires après 15 minutes d’inactivité ou 2 heures au total, selon la première échéance atteinte.

#### Scenario: Inactivité ordinaire
- **WHEN** une session ordinaire atteint 60 minutes sans activité admissible sous politique par défaut
- **THEN** elle expire même si son plafond absolu de 12 heures n’est pas atteint

#### Scenario: Plafond administratif
- **WHEN** une session d’administration ordinaire atteint 2 heures sous politique par défaut malgré une activité récente
- **THEN** elle expire sans prolongation par activité ou renouvellement
~~~~

### Référence courante authentication-81737f3de29d

Source : [authentication](../../specs/authentication/spec.md), ligne 148. SHA-256 : `81737f3de29d72442f51ae6348d6bb37f1f9c77ad8a1e8be88a48c9ee92c864c`.

Scénarios : Validité restante courte; Fraîcheur insuffisante.

~~~~text
### Requirement: Durée des accès et fraîcheur sensible

Le profil local MUST limiter par défaut les jetons d’accès API/CLI à 15 minutes et à la validité restante applicable. Une opération sensible MUST exiger par défaut une authentification datant de moins de 5 minutes et les niveaux d’assurance réellement requis, sans assurance inventée.

#### Scenario: Validité restante courte
- **WHEN** la session expire dans moins de 15 minutes lors d’une émission
- **THEN** le jeton n’est utilisable que pendant cette validité restante ou moins

#### Scenario: Fraîcheur insuffisante
- **WHEN** un compte ordinaire demande une action sensible avec une authentification datant de 5 minutes ou davantage sous politique par défaut
- **THEN** une réauthentification conforme est exigée avant l’effet sensible
~~~~

### Référence courante authentication-f87c04c0556b

Source : [authentication](../../specs/authentication/spec.md), ligne 160. SHA-256 : `f87c04c0556b341cb92597841c34d9e807d1f8c22616297f4d9c080786d16c21`.

Scénarios : Politique résolue.

~~~~text
### Requirement: Politique configurable et exceptions canoniques

Durées, fraîcheur et plafonds de sessions MUST être configurables par politique typée/versionnée exposant valeur effective et origine. Les exceptions canoniques du seul Super Admin MUST rester préservées sans s’étendre aux administrateurs ordinaires ni fabriquer d’assurance. Une invalidation courante MUST pouvoir écourter la validité annoncée.

#### Scenario: Politique résolue
- **WHEN** une politique qualifiée remplace une valeur par défaut pour un compte ordinaire
- **THEN** la valeur effective et son origine sont connues et les invalidations courantes restent applicables
~~~~

### Référence courante authentication-9f0d9b2938e0

Source : [authentication](../../specs/authentication/spec.md), ligne 168. SHA-256 : `9f0d9b2938e0078c3c7651c6b233cd9389a05e53f520757d3abfe7bc3c47b82e`.

Scénarios : Rotation réussie.

~~~~text
### Requirement: Renouvellement rotatif à usage unique

Le renouvellement API/CLI MUST employer un jeton à usage unique remplacé atomiquement à chaque renouvellement réussi. Il MUST NOT repousser le plafond absolu de session ni la date réelle d’authentification. Les secrets de renouvellement MUST rester soumis au stockage serveur par empreinte.

#### Scenario: Rotation réussie
- **WHEN** un renouvellement valide est confirmé
- **THEN** le jeton consommé ne peut plus produire de rotation et ni plafond absolu ni date réelle d’authentification ne changent
~~~~

### Référence courante authentication-c668081af427

Source : [authentication](../../specs/authentication/spec.md), ligne 176. SHA-256 : `c668081af427760a2493d4ef49fcd94f345856622ce643611155d404409b2b7f`.

Scénarios : Renouvellements seuls.

~~~~text
### Requirement: Activité utilisateur et renouvellement

Les activités repoussant l’inactivité MUST être déclarées et contrôlées côté serveur. Le renouvellement seul MUST NOT compter comme activité utilisateur. Les appels d’arrière-plan et répétitions automatiques MUST NOT être assimilés implicitement à une action utilisateur.

#### Scenario: Renouvellements seuls
- **WHEN** un client renouvelle périodiquement sans activité utilisateur admissible
- **THEN** la session expire à son échéance d’inactivité sans prolonger son plafond absolu
~~~~

### Référence courante authentication-d9131b3941bf

Source : [authentication](../../specs/authentication/spec.md), ligne 184. SHA-256 : `d9131b3941bf08793306fab4517439636b39bd5ecd125aa4447132d5fe02a079`.

Scénarios : Deux appels concurrents; Réponse perdue.

~~~~text
### Requirement: Concurrence et réponse perdue de rotation

Les concurrences et répétitions reconnues MUST NOT émettre un second renouvellement pour un jeton consommé. La perte d’une réponse MAY imposer une nouvelle authentification ; le système MUST NOT promettre la restitution d’un nouveau secret conservé seulement sous empreinte.

#### Scenario: Deux appels concurrents
- **WHEN** deux requêtes consomment le même jeton de renouvellement
- **THEN** au plus une rotation est confirmée, sans seconde émission

#### Scenario: Réponse perdue
- **WHEN** une rotation est committée mais sa réponse contenant le nouveau secret est perdue
- **THEN** la reprise ne produit pas de second renouvellement et peut imposer une nouvelle authentification
~~~~

### Référence courante authentication-4cc4a81801fe

Source : [authentication](../../specs/authentication/spec.md), ligne 196. SHA-256 : `4cc4a81801fed7394b154b348da874c29516d322e8e5288aea33f7ff7c2971b4`.

Scénarios : Réutilisation suspecte.

~~~~text
### Requirement: Réutilisation suspecte et révocation de session

Une réutilisation suspecte d’un jeton consommé MUST révoquer la session concernée et tous ses jetons dérivés, sans fermeture automatique des autres sessions du compte. Une déconnexion globale MAY être décidée par traitement d’incident autorisé. La détection MUST distinguer répétitions reconnues et concurrences légitimes d’une réutilisation suspecte selon un contrat explicite, sans seconde émission.

#### Scenario: Réutilisation suspecte
- **WHEN** le mécanisme qualifié classe une réutilisation comme suspecte
- **THEN** la session et ses dérivés sont invalidés, les autres sessions restant ouvertes sauf révocation globale autorisée
~~~~

### Référence courante authentication-42558d8e901e

Source : [authentication](../../specs/authentication/spec.md), ligne 204. SHA-256 : `42558d8e901e94ebdf8e0abd69aaa8e9830c307de5ec9bde97ba1bad0887be8a`.

Scénarios : Limite atteinte; Admissions concurrentes.

~~~~text
### Requirement: Plafond et remplacement explicite des sessions

La politique par défaut MUST limiter un compte à 5 sessions ordinaires et 2 sessions d’administration ordinaires selon leur catégorie, avec admission contrôlée atomiquement. À la limite atteinte, une admission MUST exiger le choix explicite d’une session à fermer ou être refusée ; elle MUST NOT déconnecter silencieusement une session existante.

#### Scenario: Limite atteinte
- **WHEN** une sixième session ordinaire est demandée sous politique par défaut sans remplacement choisi
- **THEN** l’admission est refusée sans fermeture silencieuse

#### Scenario: Admissions concurrentes
- **WHEN** plusieurs admissions tentent de consommer le dernier emplacement autorisé
- **THEN** le contrôle atomique empêche de dépasser le plafond effectif
~~~~

### Référence courante authentication-3f508363903c

Source : [authentication](../../specs/authentication/spec.md), ligne 216. SHA-256 : `3f508363903c83e248e623634a98c7e2d622c21b85c8404ba0c2265194c4e43e`.

Scénarios : Même cookie.

~~~~text
### Requirement: Onglets et renouvellements sans nouvelle session

Les onglets partageant le même cookie et le renouvellement de jetons MUST NOT compter comme de nouvelles sessions.

#### Scenario: Même cookie
- **WHEN** plusieurs onglets partagent une session ou un client renouvelle ses jetons
- **THEN** aucun emplacement supplémentaire n’est consommé par cette seule opération
~~~~

### Référence courante authentication-1f281505aa1c

Source : [authentication](../../specs/authentication/spec.md), ligne 224. SHA-256 : `1f281505aa1cbeb35700a343e55f4d6701cf68afde6319018d2213d14c7fff2b`.

Scénarios : Changement authentifié par défaut; Autre identité du même individu.

~~~~text
### Requirement: Changement de mot de passe sans reconnexion automatique

Le changement de mot de passe MUST être piloté par Auth depuis un PBO habilité. Le profil MUST distinguer les contextes : changement authentifié révoquant par défaut les autres sessions avec conservation possible de la session courante après vérification ; récupération/réinitialisation révoquant toutes les sessions de l'identité par défaut. La politique MAY être ajustée explicitement ; une reconnexion ou assurance supérieure MUST NOT être déduite du changement.

#### Scenario: Changement authentifié par défaut

- **WHEN** une identité change son mot de passe depuis sa session vérifiée
- **THEN** les autres sessions sont révoquées et seule la session courante peut être conservée après vérification.

#### Scenario: Autre identité du même individu

- **WHEN** le mot de passe d’une identité courante change
- **THEN** les sessions de son identité administrative suivent leur politique propre.
~~~~

### Référence courante authentication-7e9531288ce6

Source : [authentication](../../specs/authentication/spec.md), ligne 238. SHA-256 : `7e9531288ce64316cfddf0506c1d9975462ae617e35a8fbf9c4242863ba99af3`.

Scénarios : Récupération sans MFA; Changement non confirmé.

~~~~text
### Requirement: Récupération et compromission du mot de passe

Récupération et réinitialisation MUST suivre leur profil et révoquer toutes les sessions de l'identité par défaut ; une compromission suspectée MUST déclencher le retrait prévu sans assurance restaurée implicitement. Un retrait d'accès malgré panne d'audit MUST suivre audit et MUST NOT confirmer un justificatif non committé. Les tickets Kerberos déjà délivrés MUST être traités séparément des sessions Pixs.

#### Scenario: Récupération sans MFA

- **WHEN** une récupération autorisée ne fournit pas de nouvelle preuve MFA
- **THEN** les sessions sont révoquées selon le profil sans assurance multifacteur inventée.

#### Scenario: Changement non confirmé

- **WHEN** seul le retrait est confirmé après échec de mutation
- **THEN** aucun nouveau mot de passe n’est annoncé committé.
~~~~

### Référence courante authentication-2e7a00ac3949

Source : [authentication](../../specs/authentication/spec.md), ligne 252. SHA-256 : `2e7a00ac394982673813c45e4cd841e62718a07c313e0f34c219259c623bc201`.

Scénarios : Paramètres qualifiés.

~~~~text
### Requirement: Argon2id via les outils Django

Le profil local MUST protéger les mots de passe avec Argon2id via Django et argon2-cffi, avec versions stables épinglées et paramètres qualifiés pour les versions Python supportées. Il MUST NOT implémenter d’algorithme de hachage personnalisé ni abaisser sa protection pour une intégration.

#### Scenario: Paramètres qualifiés
- **WHEN** une version du profil local est préparée pour réalisation
- **THEN** la compatibilité des versions et les coûts mémoire/calcul sont qualifiés sans dépendance installée par la seule spécification
~~~~

### Référence courante authentication-82591f961338

Source : [authentication](../../specs/authentication/spec.md), ligne 260. SHA-256 : `82591f961338092914e2d8de89cb0b6bbbbce1dd8dc62dcefd49c3e3b5fcafaa`.

Scénarios : Vérification croisée; Profil incompatible.

~~~~text
### Requirement: Réutilisation Argon2id dans un profil OpenLDAP qualifié

La réutilisation d’une empreinte Argon2id par un futur profil OpenLDAP sélectionné MUST être qualifiée avec son module Argon2 et une adaptation d’enveloppe préservant variante, version, paramètres, sel et résultat. Un format ou paramètre incompatible MUST être refusé explicitement, sans repli vers un hachage plus faible.

#### Scenario: Vérification croisée
- **WHEN** un profil OpenLDAP sélectionné est qualifié pour l’empreinte produite par Django
- **THEN** la même empreinte adaptée accepte le bon mot de passe et refuse le mauvais sans réhachage ni affaiblissement

#### Scenario: Profil incompatible
- **WHEN** une variante, version, enveloppe ou un paramètre n’est pas accepté
- **THEN** la compatibilité est refusée sans hachage affaibli ni succès de qualification annoncé
~~~~

### Référence courante authentication-882a416b3157

Source : [authentication](../../specs/authentication/spec.md), ligne 272. SHA-256 : `882a416b3157563873d5b14a3e5b0eed2f5c221c9d1a0dae4b428cb3aa0b76bf`.

Scénarios : Compatibilité documentaire seule.

~~~~text
### Requirement: Limites de la compatibilité des empreintes

L’adaptation d’enveloppe MUST NOT être présentée comme récupération du mot de passe ou conversion en clé Kerberos ou Active Directory. Elle MUST NOT activer un annuaire ni dupliquer des justificatifs implicitement. PostgreSQL MUST rester distingué comme stockage applicatif de l’empreinte, sans assimilation à l’authentification de ses comptes techniques.

#### Scenario: Compatibilité documentaire seule
- **WHEN** la possibilité de réutilisation est documentée
- **THEN** aucun service LDAP, copie de justificatif, conversion de clé ou changement d’authentification PostgreSQL n’est engagé
~~~~

### Référence courante authentication-38870e5fe1b2

Source : [authentication](../../specs/authentication/spec.md), ligne 280. SHA-256 : `38870e5fe1b2ac82daab211930be3664bb27d3741bf88ae5d3d3cf87696cbda9`.

Scénarios : Trousseau indisponible.

~~~~text
### Requirement: Conservation du renouvellement de la CLI interactive

La CLI interactive MUST conserver le jeton entre lancements uniquement dans un trousseau système disponible et qualifié. Sinon, elle MUST le garder en mémoire jusqu’à la fin du processus et MUST NOT se rabattre automatiquement sur un fichier en clair. Cette conservation MUST respecter expiration, révocation et plafonds ; elle MUST NOT créer de session permanente ni de compte de service.

#### Scenario: Trousseau indisponible
- **WHEN** aucun trousseau qualifié n’est utilisable
- **THEN** le jeton reste en mémoire du processus et le lancement suivant demande une nouvelle connexion sans fichier de repli clair
~~~~

### Référence courante authentication-c423b942ab64

Source : [authentication](../../specs/authentication/spec.md), ligne 288. SHA-256 : `c423b942ab644a30f93169d10aa6bd81b22d954b9e68c9d3daca9602915a6c12`.

Scénarios : Deux identités.

~~~~text
### Requirement: Mot de passe commun par identité numérique

Une identité numérique MUST utiliser un mot de passe commun pour ses méthodes PG/LDAP/Kerberos qui en emploient un. Auth MUST coordonner les représentations de vérification et clés propres à ces méthodes, sans supposer une conversion depuis un hash PG. Les identités distinctes d'un individu MUST garder leurs propres moyens et profils.

#### Scenario: Deux identités

- **WHEN** un individu possède des comptes courant et administratif
- **THEN** le mot de passe commun concerne les méthodes de chaque identité sans imposer un secret unique à l’individu.
~~~~

### Référence courante authentication-29ea6c6bc11d

Source : [authentication](../../specs/authentication/spec.md), ligne 297. SHA-256 : `29ea6c6bc11d3ae5e1875c9a8e241f44fbfdfe8ec3d56da3a7e99f56657bd2f3`.

Scénarios : Changement natif non prévu.

~~~~text
### Requirement: Changement uniquement depuis PBO

Les mots de passe des individus MUST être changés depuis PBO sous pilotage Auth. Le PBO logique Standalone MUST pouvoir porter cette fonction ; en Domaine elle MAY être sur le contrôleur ou un autre PBO habilité. Les rotations de secrets machine et services MUST rester distinctes de cette règle.

#### Scenario: Changement natif non prévu

- **WHEN** une application tente d’utiliser une voie native non autorisée pour changer le mot de passe individuel
- **THEN** la voie est refusée ou non proposée sans contourner PBO.
~~~~

### Référence courante authentication-7507cdda1859

Source : [authentication](../../specs/authentication/spec.md), ligne 306. SHA-256 : `7507cdda1859125274e06238f7d348ba6c33cd46ad35ee7dcca99d5c58883259`.

Scénarios : Récupération non activée.

~~~~text
### Requirement: Récupération configurable et désactivée par défaut

Auth MUST proposer changement individuel, réinitialisation par administrateur habilité et récupération autonome configurable/débrayable. La récupération autonome MUST être désactivée par défaut et ses moyens activés explicitement par profil. Les politiques de mot de passe MUST pouvoir se décliner Instance/Domaine/profil, les domaines et profils ajoutant leurs contraintes au socle.

#### Scenario: Récupération non activée

- **WHEN** un individu demande le parcours autonome avec le profil par défaut
- **THEN** ce parcours reste désactivé sans créer de moyen de récupération implicite.
~~~~

### Référence courante authentication-d40c9ae62ea3

Source : [authentication](../../specs/authentication/spec.md), ligne 315. SHA-256 : `d40c9ae62ea3f70ab8ef2d36d2825a4ecb4325fa03070ff893dfa97e3b1a5af0`.

Scénarios : Chemin non qualifié.

~~~~text
### Requirement: MFA choisie par profil et chemins qualifiés

La MFA MUST être configurable par profil, y compris administratif, sans obligation générale Pixs. TOTP et clés/passkeys MUST être sélectionnables sur les chemins qualifiés ; un profil exigeant MFA MUST refuser un chemin incapable de fournir l'assurance. Gestion des facteurs MUST pouvoir être individuelle ou administrative sous habilitations et profil.

#### Scenario: Chemin non qualifié

- **WHEN** un profil exige MFA sur un chemin non qualifié
- **THEN** l’authentification est refusée sans annoncer la MFA depuis un seul facteur.
~~~~

### Référence courante authentication-d30f23cea222

Source : [authentication](../../specs/authentication/spec.md), ligne 324. SHA-256 : `d30f23cea2223420259e854f754eb651f4a3fa985cd87a85e72a01913ae10ea9`.

Scénarios : Contrôleur isolé encore actif.

~~~~text
### Requirement: Changements effectifs et contrôleurs à jour

Chaque profil MUST choisir entre confirmation de tous les contrôleurs déclarés ou de ceux maintenus en service après exclusion effective vérifiée des autres. Un défaut général MUST NOT être déduit. Le simple défaut de joignabilité MUST NOT prouver l'exclusion ni diminuer le minimum synchrone PG. La réadmission MUST être manuelle ou automatique selon profil après vérification identité, habilitations et révisions.

#### Scenario: Contrôleur isolé encore actif

- **WHEN** un contrôleur non à jour reste susceptible d’authentifier sur un réseau isolé
- **THEN** le changement n’est pas déclaré effectif tant que sa mise à jour ou son exclusion exigée n’est pas prouvée.
~~~~

### Référence courante authentication-19aff870d368

Source : [authentication](../../specs/authentication/spec.md), ligne 333. SHA-256 : `19aff870d36851592c71fafd88873fdc25c0e118a6ae19c842f1789d5090f6a7`.

Scénarios : Échecs sur LDAP.

~~~~text
### Requirement: Verrouillage commun et états dépendants

Les méthodes PG/LDAP/Kerberos concernées MUST coordonner un verrouillage par identité numérique. Les autres identités de l'individu MUST garder leurs états, sauf suspension globale Core. Les accès et mandats dépendants MUST suivre les révocations et continuités de zt-instances sans repli permissif.

#### Scenario: Échecs sur LDAP

- **WHEN** les échecs atteignent la limite applicable à l’identité via LDAP
- **THEN** le même état de verrouillage s’applique aux autres méthodes concernées sans verrouiller une autre identité par déduction.
~~~~
<!-- ACL-PIXS-2026-10-31-E3-R1:end -->

Ce fichier est une copie de référence pour préparer le lot, pas un delta OpenSpec ni une source de vérité indépendante. Les blocs complets ci-dessous conservent conditions, scénarios, valeurs validées et indications historiques. Le canon courant prévaut ; toute dérive impose une relecture avant réalisation.

La présence d’un bloc ne prouve ni applicabilité à tout profil, ni exécution, ni fonction manquante. Les lignes NE et les structures déjà livrées restent à auditer/réutiliser. Les dérogations applicatives et contrats structurels gardent leurs frontières.

## Traçabilité

| Source / ligne | Exigence | Statut de matrice | Disposition |
|---|---|---|---|
| directory-projections / 98 | [Consultation avec préférence LDAP et repli PostgreSQL](../../specs/directory-projections/spec.md#L98) | NE | AUDIT_AVANT_CREATION |
| directory-projections / 113 | [Fraîcheur après mutation et cohérence de lecture](../../specs/directory-projections/spec.md#L113) | NE | AUDIT_AVANT_CREATION |
| directory-projections / 126 | [Autorisation et confidentialité préservées à la consultation](../../specs/directory-projections/spec.md#L126) | NE | AUDIT_AVANT_CREATION |
| testing / 75 | [Conformité des projections d'annuaire optionnelles](../../specs/testing/spec.md#L75) | P | COMPLETER_OU_INTEGRER |

## Blocs sources complets

Les délimitations textuelles empêchent de confondre ces copies avec des changements normatifs. Les prescriptions et bornes restent à respecter dans leurs rôles ; toute mention historique « aucun fichier créé » appartient au contrat source et ne décrit pas l’état présent du dépôt.

### Référence directory-projections--413edead5b

Source : `openspec/specs/directory-projections/spec.md`, ligne 98. SHA-256 du bloc : `3784cdbf3d9275cbb4ab94e88ef6a8be2089c0e91281d4ad7675014b7c402929`.

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

### Référence directory-projections--982789bee3

Source : `openspec/specs/directory-projections/spec.md`, ligne 113. SHA-256 du bloc : `6fac9d275fc1c5b74bd74fd52c20d1a7495dcd3e61de56f750f1e845b61c7d55`.

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

### Référence directory-projections--1354b903ea

Source : `openspec/specs/directory-projections/spec.md`, ligne 126. SHA-256 du bloc : `88316b878b5cf270b173aa29d5413aba9e09f4dd6824bf202f7e67e98cfcca82`.

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

